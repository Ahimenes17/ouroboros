def draw_ascii_map(landscape):
    """Создать простую ASCII-карту ландшафта (без сложных шаблонов)."""
    symbols = landscape['visual_symbols']
    center = symbols[0]
    terrain_char = landscape['terrain_type'][0]
    npc_name = landscape['npc'][:8]

    lines = []
    lines.append("  ┌─────────────┐")
    lines.append(f"  │ {symbols[1]}           {symbols[2]} │")
    lines.append("  │             │")
    lines.append(f"  │    {center}     │")
    lines.append("  │             │")
    lines.append(f"  │   {terrain_char*3}   {terrain_char*3} │")
    lines.append(f"  │   {npc_name:<8}   │")
    lines.append("  │ Достопр.    │")
    lines.append("  │ Опасность   │")
    lines.append("  └─────────────┘")
    return "\n".join(lines)