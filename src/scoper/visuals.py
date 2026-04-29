import math
from typing import Dict

def generate_nexus_radar_chart(coverage: Dict[str, bool]) -> str:
    """Generate a glowing SVG radar chart for the Nexus Index."""
    # Axes: GOV, RES, INT, PRI, SOV, ID
    # Map them to 6 points
    axes = ["P_GOV", "P_RES", "P_INT", "P_PRI", "P_SOV", "P_ID"]
    labels = ["GOV", "RES", "INT", "PRI", "SOV", "ID"]
    
    # SVG Dimensions
    size = 300
    center_x = size / 2
    center_y = size / 2
    max_radius = 100
    
    points = []
    bg_points = []
    inner_bg_points = []
    
    for i in range(6):
        angle = math.pi / 2 - (i * 2 * math.pi / 6)
        
        # Max radius points for background grid
        bx = center_x + max_radius * math.cos(angle)
        by = center_y - max_radius * math.sin(angle)
        bg_points.append(f"{bx},{by}")
        
        # Inner radius points for background grid
        ix = center_x + (max_radius * 0.5) * math.cos(angle)
        iy = center_y - (max_radius * 0.5) * math.sin(angle)
        inner_bg_points.append(f"{ix},{iy}")
        
        # Data points
        axis_key = axes[i]
        val = coverage.get(axis_key, False)
        # If true, 100% radius, if false, 20% radius (so it doesn't just disappear to the center)
        r = max_radius if val else (max_radius * 0.2)
        x = center_x + r * math.cos(angle)
        y = center_y - r * math.sin(angle)
        points.append(f"{x},{y}")
        
    points_str = " ".join(points)
    bg_points_str = " ".join(bg_points)
    inner_bg_points_str = " ".join(inner_bg_points)
    
    # Generate labels
    labels_svg = ""
    for i, label in enumerate(labels):
        angle = math.pi / 2 - (i * 2 * math.pi / 6)
        r = max_radius + 25
        x = center_x + r * math.cos(angle)
        y = center_y - r * math.sin(angle)
        # Adjust text alignment based on position
        anchor = "middle"
        if abs(math.cos(angle)) > 0.1:
            anchor = "start" if math.cos(angle) > 0 else "end"
            
        labels_svg += f'<text x="{x}" y="{y + 4}" font-family="Outfit, sans-serif" font-size="10px" font-weight="700" fill="#94a3b8" text-anchor="{anchor}" letter-spacing="1px">{label}</text>\n'

    # Lines from center to axes
    axis_lines = ""
    for pt in bg_points:
        axis_lines += f'<line x1="{center_x}" y1="{center_y}" x2="{pt.split(",")[0]}" y2="{pt.split(",")[1]}" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>\n'

    svg = f"""
    <svg width="100%" height="100%" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <filter id="neon-glow" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
          <feMerge>
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
        <linearGradient id="poly-grad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="rgba(0, 240, 255, 0.4)" />
          <stop offset="100%" stop-color="rgba(59, 130, 246, 0.1)" />
        </linearGradient>
      </defs>
      
      <!-- Background Grids -->
      <polygon points="{bg_points_str}" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="1"/>
      <polygon points="{inner_bg_points_str}" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="1"/>
      {axis_lines}
      
      <!-- Data Polygon -->
      <polygon points="{points_str}" fill="url(#poly-grad)" stroke="#00f0ff" stroke-width="2" filter="url(#neon-glow)"/>
      
      <!-- Data Points -->
      """
    
    for pt in points:
        svg += f'<circle cx="{pt.split(",")[0]}" cy="{pt.split(",")[1]}" r="4" fill="#020617" stroke="#00f0ff" stroke-width="2" filter="url(#neon-glow)"/>\n'

    svg += labels_svg
    svg += "</svg>"
    
    return svg
