import {useState, useEffect} from "react"
import './App.css'
import {groupTablesByArea, groupTablesBySection} from "./utils/tableGrouping.js";
import RestaurantTable from "./components/RestaurantTable.jsx";

function App() {
    const [tables, setTables] = useState([])

    const {inside, outside} = groupTablesByArea(tables);
    const insideSections = groupTablesBySection(inside);
    const outsideSections = groupTablesBySection(outside)

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
        <p>Restaurant Seating Management System</p>
          <h2>Inside</h2>
          {
              Object.entries(insideSections).map(([sectionId, sectionTables]) => (
                  <div key = {sectionId}>
                      <h3>Section {sectionId}</h3>

                      {sectionTables.map( (table) => (
                          <RestaurantTable
                          key={table.table_number}
                          table = {table}
                          />
                      ))}


                  </div>
                  )
              )
          }

          <h2>Outside</h2>
          {
              Object.entries(outsideSections).map(([sectionId, sectionTables]) => (
                  <div key = {sectionId}>
                      <h3>Section {sectionId}</h3>

                      {sectionTables.map( (table) => (
                          <RestaurantTable
                          key={table.table_number}
                          table = {table}
                          />
                      ))}
                  </div>
              ))
          }
      </div>
    )
}

export default App