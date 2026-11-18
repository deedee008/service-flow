export function groupTablesByArea(tables) {
    const inside = tables.filter((table) =>
        table.section_id === 1 ||
        table.section_id === 2 ||
        table.section_id === 3
    );
    const outside = tables.filter((table) =>
        table.section_id === 4 ||
        table.section_id ===5
    );

    return {inside, outside}
}

export function groupTablesBySection(tables) {
    return Object.groupBy(tables, (table) => table.section_id)
}