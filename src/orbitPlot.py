import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def display_orbit(planet_name, pl_orbsmax, pl_orbeccen, pl_orbper,hostname):

    # Check that both measurements exist
    a = pd.to_numeric(pl_orbsmax, errors="coerce")
    e = pd.to_numeric(pl_orbeccen, errors="coerce")
    period = pd.to_numeric(pl_orbper, errors="coerce")

    if pd.isna(period) or period <= 0:
        st.warning("Orbital animation unavailable: orbital period is missing.")
        return

    if pd.isna(a) or pd.isna(e):
        st.warning("Orbital visualisation unavailable: missing orbital radius or eccentricity.")
        return

    # Validate measurements
    if a <= 0 or not 0 <= e < 1:
        st.warning("Orbital visualisation unavailable: invalid orbital measurements.")
        return

    # Calculate ellipse
    theta = np.linspace(0, 2 * np.pi, 500)

    # Polar equation of an ellipse with the star at one focus
    r = (a * (1 - e**2)) / (1 + e * np.cos(theta))

    x = r * np.cos(theta)
    y = r * np.sin(theta)

    fig = go.Figure()

    frames = []

    frame_count = 100
    repeat_count = 20

    frame_duration_ms = max(
        20,
        int(period * 20 / frame_count)
    )

    for cycle in range(repeat_count):

        mean_anomalies = np.linspace(
            0,
            2 * np.pi,
            frame_count,
            endpoint=False
        )

        for mean_anomaly in mean_anomalies:

            # Solve Kepler's equation
            eccentric_anomaly = mean_anomaly

            for _ in range(10):
                eccentric_anomaly -= (
                                             eccentric_anomaly
                                             - e * np.sin(eccentric_anomaly)
                                             - mean_anomaly
                                     ) / (1 - e * np.cos(eccentric_anomaly))

            # Calculate planet position
            planet_x = a * (np.cos(eccentric_anomaly) - e)
            planet_y = a * np.sqrt(1 - e ** 2) * np.sin(eccentric_anomaly)

            # Calculate elapsed orbital days
            elapsed_days = (mean_anomaly / (2 * np.pi)) * period

            frames.append(
                go.Frame(
                    data=[
                        go.Scatter(
                            x=[planet_x],
                            y=[planet_y]
                        ),
                        go.Scatter(
                            text=[f"Day {elapsed_days:.1f} / {period:.1f}"]
                        )
                    ],
                    traces=[2, 3],
                    name=str(len(frames))
                )
            )

    fig.frames = frames


    periapsis = a * (1 - e)
    apoapsis = a * (1 + e)

    fig.add_annotation(
        x=0,
        y=a,
        text=f"Orbit: {periapsis:.3f}AU by {apoapsis:.3f}AU",
        showarrow=False,
        yshift=20,
        font=dict(
            color="#FFFFFF",
            size=13
        ))


    # Orbital path
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode="lines",
        name="Orbital path",
        line=dict(color="#D92906", width=2)
    ))

    # Host star at the focus
    fig.add_trace(go.Scatter(
        x=[0],
        y=[0],
        mode="markers",
        name=hostname,
        marker=dict(size=18, color="#FFD166", symbol="star")
    ))

    # Planet
    fig.add_trace(go.Scatter(
        x=[a * (1 - e)],
        y=[0],
        mode="markers",
        name=planet_name,
        marker=dict(size=12, color="#69B7F0")
    ))

    # Days counter in bottom-left
    x_limit = a * (1 + e) * 1.25
    y_limit = a * np.sqrt(1 - e ** 2) * 1.35

    fig.add_trace(go.Scatter(
        x=[-x_limit * 0.92],
        y=[-y_limit * 0.90],
        mode="text",
        text=["Day 0.0"],
        textposition="bottom right",
        textfont=dict(
            color="#FFFFFF",
            size=13
        ),
        showlegend=False,
        hoverinfo="skip"
    ))

    fig.update_layout(
        title=f"Orbit of {planet_name}",
        height=450,
        paper_bgcolor="#080D1A",
        plot_bgcolor="#080D1A",
        font_color="#FF00FF",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=10, r=10, t=50, b=65),
        xaxis=dict(
            visible=False,
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[-x_limit, x_limit],
            scaleanchor="y",
            scaleratio=1
        ),
        yaxis=dict(
            visible=False,
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[-y_limit, y_limit]
        ),
        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                x=0.5,
                y=-0.22,
                xanchor="center",
                bgcolor="#D92906",
                bordercolor="#D92906",
                font=dict(
                    color="#FFFFFF",
                    size=13
                ),
                buttons=[
                    dict(
                        label="▶ Play",
                        method="animate",
                        args=[
                            None,
                            {
                                "frame": {
                                    "duration": frame_duration_ms,
                                    "redraw": True
                                },
                                "fromcurrent": True,
                                "transition": {"duration": 0},
                                "mode": "immediate"
                            }
                        ]
                    ),
                dict(
                    label="⏸ Pause",
                    method="animate",
                    args=[
                        [None],
                        {
                            "frame": {"duration": 0, "redraw": False},
                            "mode": "immediate",
                            "transition": {"duration": 0}
                        }
                    ]
                )
            ]
        )
    ]

    )

    st.plotly_chart(fig, use_container_width=True)