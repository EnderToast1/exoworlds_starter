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

    skipped = len(system) - len(orbiters)
    if skipped:
        st.caption(
            f"Showing {len(orbiters)} of {len(system)} planets around "
            f"{hostname}; {skipped} missing usable orbital measurements."
        )
    elif len(orbiters) > 1:
        st.caption(f"Showing all {len(orbiters)} planets around {hostname}.")

    # Sort inner → outer so legend/colours stay readable.
    orbiters = sorted(orbiters, key=lambda o: o["a"])

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

    max_extent = 0.0

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

        apoapsis = orbiter["a"] * (1 + orbiter["e"])
        max_extent = max(max_extent, apoapsis)

    fig.add_trace(go.Scatter(
        x=[0],
        y=[0],
        mode="markers",
        name=str(hostname),
        marker=dict(size=18, color="#FFD166", symbol="star"),
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
            textfont=dict(color="#FFFFFF", size=11),
            marker=dict(
                size=14 if is_selected else 10,
                color=colour,
                line=dict(width=2 if is_selected else 0, color="#FFFFFF"),
            ),
        ))

    x_limit = max_extent * 1.25
    y_limit = max_extent * 1.25

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
    fig.add_annotation(
        x=0,
        y=max_extent,
        text=(
            f"{reference['name']}: {periapsis:.3f}–{apoapsis:.3f} AU"
            if selected
            else f"System span: {max_extent:.3f} AU"
        ),
        showarrow=False,
        yshift=20,
        font=dict(color="#FFFFFF", size=13),
    )

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

    for _ in range(repeat_count):
        for step in range(frame_count):
            # Shared system clock in days, one loop = one orbit of the reference planet.
            elapsed_days = (step / frame_count) * reference["period"]
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
                        f"Day {elapsed_days:.1f} / {reference['period']:.1f}"
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
        height=450,
        paper_bgcolor="#080D1A",
        plot_bgcolor="#080D1A",
        font_color="#FFFFFF",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.18,
            xanchor="center",
            x=0.5,
        ),
        margin=dict(l=10, r=10, t=50, b=80),
        xaxis=dict(
            visible=False,
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[-x_limit, x_limit],
            scaleanchor="y",
            scaleratio=1,
        ),
        yaxis=dict(
            visible=False,
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[-y_limit, y_limit],
        ),
        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                x=0.5,
                y=-0.28,
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
