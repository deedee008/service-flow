export default function RestaurantTable ( { table }) {
    return (
        <div className = "table_wrapper">
            <button className = "table_button">
                {table.table_number}
            </button>

            {Array.from( {length: table.capacity}, (_, index) => (
                    <span
                        key={index}
                        className="seat"
                        style = {{
                            left: `${50 + 42 * Math.cos((2 * Math.PI * index) / table.capacity)}%`,
                            top: `${50 + 42 * Math.sin((2 * Math.PI * index) / table.capacity)}%`
                    }}
                    />
            ))}
        </div>
    );
}