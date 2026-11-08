import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


PLANET_COLOURS = [
    "#69B7F0",
    "#50C878",
    "#FFD166",
    "#E07A5F",
    "#9B5DE5",
    "#00BBF9",
    "#F15BB5",
    "#FEE440",
]


def _kepler_position(a, e, mean_anomaly):
    """Return (x, y) for an elliptical orbit with the star at one focus."""
    eccentric_anomaly = mean_anomaly

    for _ in range(10):
        eccentric_anomaly -= (
            eccentric_anomaly
            - e * np.sin(eccentric_anomaly)
            - mean_anomaly
        ) / (1 - e * np.cos(eccentric_anomaly))

    x = a * (np.cos(eccentric_anomaly) - e)
    y = a * np.sqrt(1 - e ** 2) * np.sin(eccentric_anomaly)
    return x, y


def _ellipse_path(a, e, points=500):
    """Polar ellipse path with the star at one focus."""
    theta = np.linspace(0, 2 * np.pi, points)
    r = (a * (1 - e ** 2)) / (1 + e * np.cos(theta))
    return r * np.cos(theta), r * np.sin(theta)


def _valid_orbit_row(row):
    a = pd.to_numeric(row["pl_orbsmax"], errors="coerce")
    e = pd.to_numeric(row["pl_orbeccen"], errors="coerce")
    period = pd.to_numeric(row["pl_orbper"], errors="coerce")

    if pd.isna(a) or pd.isna(e) or pd.isna(period):
        return None
    if a <= 0 or period <= 0 or not 0 <= e < 1:
        return None

    return {
        "name": str(row["pl_name"]),
        "a": float(a),
        "e": float(e),
        "period": float(period),
    }


def display_orbit(planet_name, hostname, planets):
    """Plot and animate all planets orbiting the same host star."""

    system = planets.loc[planets["hostname"] == hostname].copy()
    orbiters = []

    for _, row in system.iterrows():
        orbiter = _valid_orbit_row(row)
        if orbiter is not None:
            orbiters.append(orbiter)

    if not orbiters:
        st.warning(
            "Orbital visualisation unavailable: no planets in this system "
            "have a usable orbital radius, eccentricity and period."
        )
        return

    # Prefer the selected planet as the animation clock when it has valid data.
    selected = next((o for o in orbiters if o["name"] == planet_name), None)
    reference = selected or min(orbiters, key=lambda o: o["period"])

    # Sort inner → outer so legend/colours stay readable.
    orbiters = sorted(orbiters, key=lambda o: o["a"])

    def apoapsis_of(orbiter):
        return orbiter["a"] * (1 + orbiter["e"])

    max_extent = max(apoapsis_of(o) for o in orbiters)

    # Zoom around the selected planet so close-in orbits are not crushed
    # by a distant outer companion on a linear scale.
    focus = selected or orbiters[0]
    focus_extent = apoapsis_of(focus)
    view_span_limit = focus_extent * 2.2
    framed_extent = max(
        (apoapsis_of(o) for o in orbiters if apoapsis_of(o) <= view_span_limit),
        default=focus_extent,
    )
    # Tight framing so the selected orbit fills most of the canvas.
    view_extent = max(framed_extent * 1.2, focus_extent * 1.3)
    x_limit = view_extent
    y_limit = view_extent

    clipped_outer = sum(1 for o in orbiters if apoapsis_of(o) > view_extent)
    skipped = len(system) - len(orbiters)

    notes = []
    if skipped:
        notes.append(
            f"{skipped} planet(s) missing usable orbital measurements"
        )
    if clipped_outer:
        notes.append(
            f"zoomed to {planet_name}; {clipped_outer} outer orbit(s) "
            f"lie outside this view"
        )
    elif len(orbiters) > 1:
        notes.append(f"showing {len(orbiters)} planets around {hostname}")

    if notes:
        st.caption(" · ".join(notes).capitalize() + ".")

    fig = go.Figure()

    # Trace layout:
    # 0 .. n-1   orbital paths
    # n           host star
    # n+1 .. 2n   planet markers
    # 2n+1        day counter
    path_count = len(orbiters)
    star_trace = path_count
    first_planet_trace = star_trace + 1
    day_trace = first_planet_trace + path_count

    for i, orbiter in enumerate(orbiters):
        x, y = _ellipse_path(orbiter["a"], orbiter["e"])
        is_selected = orbiter["name"] == planet_name
        colour = PLANET_COLOURS[i % len(PLANET_COLOURS)]

        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            mode="lines",
            name=f"{orbiter['name']} path",
            line=dict(
                color=colour,
                width=3 if is_selected else 1.5,
                dash="solid" if is_selected else "dot",
            ),
            hoverinfo="skip",
            showlegend=False,
        ))

    fig.add_trace(go.Scatter(
        x=[0],
        y=[0],
        mode="markers",
        name=str(hostname),
        marker=dict(size=22, color="#FFD166", symbol="star"),
    ))

    for i, orbiter in enumerate(orbiters):
        is_selected = orbiter["name"] == planet_name
        colour = PLANET_COLOURS[i % len(PLANET_COLOURS)]
        start_x = orbiter["a"] * (1 - orbiter["e"])

        fig.add_trace(go.Scatter(
            x=[start_x],
            y=[0],
            mode="markers+text" if is_selected else "markers",
            name=orbiter["name"],
            text=[orbiter["name"]] if is_selected else None,
            textposition="top center",
            textfont=dict(color="#FFFFFF", size=12),
            marker=dict(
                size=16 if is_selected else 11,
                color=colour,
                line=dict(width=2 if is_selected else 0, color="#FFFFFF"),
            ),
        ))

    fig.add_trace(go.Scatter(
        x=[-x_limit * 0.92],
        y=[-y_limit * 0.90],
        mode="text",
        text=["Day 0.0"],
        textposition="bottom right",
        textfont=dict(color="#FFFFFF", size=13),
        showlegend=False,
        hoverinfo="skip",
    ))

    periapsis = reference["a"] * (1 - reference["e"])
    apoapsis = reference["a"] * (1 + reference["e"])


    frame_count = 100
    repeat_count = 20
    frame_duration_ms = max(
        20,
        int(reference["period"] * 20 / frame_count),
    )

    frames = []
    planet_trace_indices = list(
        range(first_planet_trace, first_planet_trace + path_count)
    )

    for cycle in range(repeat_count):
        for step in range(frame_count):
            # Continuous system clock so companions keep their place when the
            # reference planet completes an orbit and loops.
            elapsed_days = (
                (cycle * frame_count + step) / frame_count
            ) * reference["period"]
            reference_day = elapsed_days % reference["period"]
            frame_data = []

            for orbiter in orbiters:
                mean_anomaly = (
                    2 * np.pi * (elapsed_days / orbiter["period"])
                ) % (2 * np.pi)
                planet_x, planet_y = _kepler_position(
                    orbiter["a"],
                    orbiter["e"],
                    mean_anomaly,
                )
                frame_data.append(
                    go.Scatter(x=[planet_x], y=[planet_y])
                )

            frame_data.append(
                go.Scatter(
                    text=[
                        f"Day {reference_day:.1f} / {reference['period']:.1f}"
                        f" ({reference['name']})"
                    ]
                )
            )

            frames.append(
                go.Frame(
                    data=frame_data,
                    traces=planet_trace_indices + [day_trace],
                    name=str(len(frames)),
                )
            )

    fig.frames = frames

    title = (
        f"Orbits around {hostname}"
        if len(orbiters) > 1
        else f"Orbit of {orbiters[0]['name']}"
    )

    fig.update_layout(
        title=title,
        height=720,
        paper_bgcolor="#080D1A",
        plot_bgcolor="#080D1A",
        font_color="#FFFFFF",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.12,
            xanchor="center",
            x=0.5,
        ),
        margin=dict(l=20, r=20, t=60, b=100),
        xaxis=dict(
            visible=False,
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[-x_limit, x_limit],
            scaleanchor="y",
            scaleratio=1,
            constrain="domain",
        ),
        yaxis=dict(
            visible=False,
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[-y_limit, y_limit],
            constrain="domain",
        ),
        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                x=0.5,
                y=-0.20,
                xanchor="center",
                bgcolor="#D92906",
                bordercolor="#D92906",
                font=dict(color="#FFFFFF", size=13),
                buttons=[
                    dict(
                        label="▶ Play",
                        method="animate",
                        args=[
                            None,
                            {
                                "frame": {
                                    "duration": frame_duration_ms,
                                    "redraw": True,
                                },
                                "fromcurrent": True,
                                "transition": {"duration": 0},
                                "mode": "immediate",
                            },
                        ],
                    ),
                    dict(
                        label="⏸ Pause",
                        method="animate",
                        args=[
                            [None],
                            {
                                "frame": {"duration": 0, "redraw": False},
                                "mode": "immediate",
                                "transition": {"duration": 0},
                            },
                        ],
                    ),
                ],
            )
        ],
    )

    st.plotly_chart(fig, use_container_width=True)
