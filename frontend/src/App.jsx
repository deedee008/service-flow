import {useState, useEffect} from "react"
import './App.css'
import {groupTablesByArea, groupTablesBySection} from "./utils/tableGrouping.js";
import RestaurantTable from "./components/RestaurantTable.jsx";

function App() {
    const [tables, setTables] = useState([]);

    const [partySize, setPartySize] = useState("");

    const [recommendation, setRecommendation] = useState(null);

    const {inside, outside} = groupTablesByArea(tables);
    const insideSections = groupTablesBySection(inside);
    const outsideSections = groupTablesBySection(outside);

    useEffect(() => {
        fetch("http://127.0.0.1:8000/api/tables")
            .then(response => response.json())
            .then(data => {
                console.log("Tables received: ", data);
                setTables(data);
            })
            .catch(error => console.error("Error fetching tables: ", error));
    }, []);

    function handleGetRecommendation(){
        const size = Number(partySize)

        if(
            // Check if the input is empty or contains only spaces
            partySize.trim() === "" ||

            // Check if the value is not an integer
            !Number.isInteger(size) ||

            // Check if the party size is less than 1
            size < 1
        )
        {
            alert("Please enter a valid party size.");
            return;
        }

        console.log("Sending party size: ", size, typeof size)
        // Send the party size to the FastAPI backend
        fetch("http://127.0.0.1:8000/api/recommendations", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({party_size: size})
        })
            .then(response => {
                if(!response.ok){
                    return response.json().then(errorData => {
                        console.log("Backend validation error: ", errorData);
                        throw new Error("Failed to get recommendation");
                    })
                }
                return response.json();
            })
            .then(data => {
                console.log("Recommendation received: ", data);
                setRecommendation(data);
            })
            .catch(error => {
                console.error("Error getting recommendation: ", error);
            });
    }


    return (
      <div>
        <h1>ServiceFlow</h1>
        <p>Restaurant Seating Management System</p>

          <div>
              <label>Party Size: </label>
              <input
                  type = "number"
                  min = "1"
                  value = {partySize}
                  onChange = {(event) => setPartySize(event.target.value)}
              />
              <button type = "button" onClick = {handleGetRecommendation}>Get Recommendation</button>

              {recommendation && (
                  <div>
                      <h3>Seating Recommendation</h3>
                      <p>Table: {recommendation.table_number}</p>
                      <p>Server: {recommendation.server_name}</p>
                  </div>
              )}
          </div>

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