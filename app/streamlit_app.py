import streamlit as st
import pydeck as pdk

from raven.sim import RavenSimulation

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(
    page_title="RAVEN 4.1 · Deterministic Autonomy Kernel",
    layout="wide"
)

st.title("RAVEN 4.1 · Deterministic Autonomy Kernel")

# ----------------------------
# Session state
# ----------------------------
if "sim" not in st.session_state:
    st.session_state.sim = RavenSimulation()

sim = st.session_state.sim
vehicle = sim.vehicle

# ----------------------------
# Layout
# ----------------------------
left, right = st.columns([2, 1])

with left:
    trail = [
        {
            "src": [
                sim.terrain[i - 1].x,
                sim.terrain[i - 1].y,
                sim.terrain[i - 1].z,
            ],
            "dst": [seg.x, seg.y, seg.z],
            "color": [
                int(255 * seg.risk),
                int(200 * (1 - seg.risk)),
                80,
            ],
        }
        for i, seg in enumerate(sim.terrain)
        if i > 0
    ]

    st.pydeck_chart(
        pdk.Deck(
            layers=[
                pdk.Layer(
                    "LineLayer",
                    trail,
                    get_source_position="src",
                    get_target_position="dst",
                    get_color="color",
                    width_scale=2,
                ),
                pdk.Layer(
                    "ScatterplotLayer",
                    [{"pos": [vehicle.x, vehicle.y, vehicle.z]}],
                    get_position="pos",
                    get_radius=4,
                    get_fill_color=[0, 224, 164],
                ),
            ],
            initial_view_state=pdk.ViewState(
                target=[vehicle.x, vehicle.y, vehicle.z],
                zoom=1,
                pitch=55,
            ),
            map_style=None,
        )
    )

with right:
    st.markdown(f"**Mode:** {vehicle.mode}")
    st.markdown(f"**Speed:** {vehicle.speed_mps * 3.6:.1f} km/h")
    st.markdown(f"**Stability:** {vehicle.stability_index:.1f}")
    st.markdown(f"**Drift:** {vehicle.drift_score:.1f}")

    if st.button("▶ Step"):
        sim.step()
        st.rerun()

    if sim.human_lock:
        st.error("⚠️ RAVEN entered STOP_SAFE\n\nHuman attention required.")
        if st.button("Acknowledge & continue"):
            sim.human_lock = False
            st.rerun()
