import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def display_orbit(planet_name, pl_orbsmax, pl_orbeccen):

    # Check that both measurements exist
    a = pd.to_numeric(pl_orbsmax, errors="coerce")
    e = pd.to_numeric(pl_orbeccen, errors="coerce")

    if pd.isna(a) or pd.isna(e):
        st.info("Orbital visualisation unavailable: missing orbital radius or eccentricity.")
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

    for i, mean_anomaly in enumerate(np.linspace(0, 2 * np.pi, 100, endpoint=False)):

        # Solve Kepler's equation using Newton-Raphson
        eccentric_anomaly = mean_anomaly

        for _ in range(10):
            eccentric_anomaly -= (
                                         eccentric_anomaly - e * np.sin(eccentric_anomaly) - mean_anomaly
                                 ) / (1 - e * np.cos(eccentric_anomaly))

        # Calculate planet position
        planet_x = a * (np.cos(eccentric_anomaly) - e)
        planet_y = a * np.sqrt(1 - e ** 2) * np.sin(eccentric_anomaly)

        frames.append(
            go.Frame(
                data=[
                    go.Scatter(
                        x=[planet_x],
                        y=[planet_y]
                    )
                ],
                traces=[2],
                name=str(i)
            )
        )

    fig.frames = frames


    periapsis = a * (1 - e)
    apoapsis = a * (1 + e)

    fig.add_annotation(
        x=0,
        y=a,
        text=f"Orbit: {periapsis:.3f} by {apoapsis:.3f} AU",
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
        name="Host star",
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

    fig.update_layout(
        title=f"Orbit of {planet_name}",
        height=450,
        paper_bgcolor="#080D1A",
        plot_bgcolor="#080D1A",
        font_color="#FFFFFF",
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
            title="",
            visible=False,
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            scaleanchor="y",
            scaleratio=1
        ),
        yaxis=dict(
            title="",
            visible=False,
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
    updatemenus = [
        dict(
            type="buttons",
            showactive=False,
            x=0.5,
            y=-0.22,
            xanchor="center",
            buttons=[
                dict(
                    label="▶ Play",
                    method="animate",
                    args=[
                        None,
                        {
                            "frame": {"duration": 50, "redraw": True},
                            "fromcurrent": True,
                            "transition": {"duration": 0}
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