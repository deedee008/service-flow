import {useState, useEffect} from "react"
import './App.css'

function App() {
    const [tables, setTables] = useState([])

    useEffect(() => {
        fetch("http://127.0.0.1:8000/api/tables")
            .then(response => response.json())
            .then(data => {
                console.log("Tables received: ", data);
                setTables(data);
            })
            .catch(error => console.error("Error fetching tables: ", error));
    }, []);

    return (
      <div>
        <h1>ServiceFlow</h1>
          {tables.map((table) => (
              <button key={table.table_number} className="table_button">{table.table_number}</button>
          ))}
        <p>Restaurant Seating Management System</p>
      </div>
    )
}

export default App