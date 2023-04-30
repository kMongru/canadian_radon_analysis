import "./App.scss";
import React, { useState } from "react";
import removeRadon from "./removeRadon.png";
import Papa from "papaparse";

// drag drop file component
function DragDropFile(props) {
  const [status, setStatus] = props.status;
  const [results, setResults] = props.results;
  // drag state
  const [dragActive, setDragActive] = React.useState(false);
  // ref
  const inputRef = React.useRef(null);

  async function handleFile(files) {
    setStatus("loading");
    Papa.parse(files, {
      header: true,
      skipEmptyLines: true,
      complete: function (results) {
        console.log(results.data);
        const csv = results.data;
        // create urls
        const reqs = [];
        console.log(csv);
        for (const row of csv) {
          const {
            timestamp: ts,
            pressure,
            temperature: temp,
            tvoc,
            humidity: humid,
          } = row;
          reqs.push(
            `https://1jjce35g6d.execute-api.us-east-2.amazonaws.com/dev/?pressure=${pressure}&temperature=${temp}&tvoc=${tvoc}&humidity=${humid}&timestamp=${ts}`
          );
        }

        // make req
        const fetchPromises = [];
        for (const req of reqs) {
          fetchPromises.push(fetch(req));
        }

        // Define an async function to handle the fetch requests
        async function fetchAllData() {
          try {
            // Use Promise.all() to wait for all fetch promises to resolve
            const responses = await Promise.all(fetchPromises);

            // Iterate through the responses and extract the JSON data
            const data = [];
            for (const response of responses) {
              const jsonData = await response.json();
              data.push(jsonData);
            }

            // Do something with the data
            console.log(data);
            setResults(data);
            setStatus("results");
          } catch (error) {
            // Handle any errors that occur during the fetch requests
            console.error("Error fetching data:", error);
          }
        }
        fetchAllData();
      },
    });

    // setTimeout(() => {
    //   setStatus("results");
    // }, 2000);
  }

  // handle drag events
  const handleDrag = function (e) {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  // triggers when file is dropped
  const handleDrop = function (e) {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  // triggers when file is selected with click
  const handleChange = function (e) {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  // triggers the input when the button is clicked
  const onButtonClick = () => {
    inputRef.current.click();
  };

  return (
    <>
      <form
        id="form-file-upload"
        onDragEnter={handleDrag}
        onSubmit={(e) => e.preventDefault()}
      >
        <input
          ref={inputRef}
          type="file"
          id="input-file-upload"
          accept=".csv"
          onChange={handleChange}
        />
        <label
          id="label-file-upload"
          htmlFor="input-file-upload"
          className={dragActive ? "drag-active" : ""}
        >
          <div>
            <p>Drag and drop or upload your file</p>
            <button className="upload-button" onClick={onButtonClick}></button>
          </div>
        </label>
        {dragActive && (
          <div
            id="drag-file-element"
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          ></div>
        )}
      </form>
    </>
  );
}

function RenderSwitch() {
  const [status, setStatus] = useState();
  const [results, setResults] = useState();
  // const [data, setData] = useState();

  switch (status) {
    case "loading":
      function complete() {
        // Get the circle-loader element by its class name
        var circleLoader = document.querySelector(".circle-loader");

        // Get the checkmark element by its class name
        var checkmark = document.querySelector(".checkmark");

        // Toggle the 'load-complete' class on the circle-loader element
        circleLoader.classList.toggle("load-complete");

        // Toggle the visibility of the checkmark element
        checkmark.style.display = "inline";
      }

      return (
        <div style={{ margin: "20px auto" }}>
          <div className="circle-loader">
            <div className="checkmark draw"></div>
          </div>

          <p>
            <button
              onClick={complete}
              id="toggle"
              type="button"
              className="btn btn-success"
            >
              Toggle Completed
            </button>
          </p>
        </div>
      );
    case "results":
      const data = [
        { radon: 65.80246302857995, timestamp: "01-02" },
        { radon: 65.80246302857995, timestamp: "01-02" },
        { radon: 65.80246302857995, timestamp: "01-02" },
      ];
      return (
        <>
          <h1>Results</h1>
          <table style={{ margin: "20px auto" }}>
            <thead>
              <tr>
                <th>Radon</th>
                <th>Timestamp</th>
                <th>Safety</th>
              </tr>
            </thead>
            <tbody>
              {data.map((item) =>
                item.randon > 100 ? (
                  <tr
                    key={item.timestamp}
                    style={{ backgroundColor: "lightgreen" }}
                  >
                    <td>{item.radon}</td>
                    <td>{item.timestamp}</td>
                    <td>{"✅"}</td>
                  </tr>
                ) : (
                  <tr
                    key={item.timestamp}
                    style={{ backgroundColor: "lightcoral" }}
                  >
                    <td>{item.radon}</td>
                    <td>{item.timestamp}</td>
                    <td>{"⚠️"}</td>
                  </tr>
                )
              )}
            </tbody>
          </table>
        </>
      );
    default:
      return (
        <DragDropFile
          status={[status, setStatus]}
          results={[results, setResults]}
        />
      );
  }
}

function App() {
  return (
    <div>
      <img src={removeRadon} style={{ width: "400px" }} />
      {RenderSwitch()}
      <h1>How does it work?</h1>
      <ol style={{ textAlign: "left", margin: "auto", width: "28rem" }}>
        <li>
          Upload your file with the headers "temperature", "humidity",
          "pressure", "tvoc", and "state".
        </li>
        <li>Submit your file</li>
        <li>Wait to view the results!</li>
      </ol>
      <div style={{ marginTop: "5vh" }}>
        <strong>Made with ❤️ by</strong>
        <div>
          {" "}
          <a href="https://www.linkedin.com/in/juliagroza/">
            Julia Groza
          </a>,{" "}
          <a href="https://www.linkedin.com/in/rhys-dominguez/">
            Rhys Dominguez
          </a>
          ,{" "}
          <a href="https://www.linkedin.com/in/keegan-mongru/">Keegan Mongru</a>
          ,{" "}
          <a href="https://www.linkedin.com/in/cullen-macleod/">
            Cullen Macleod
          </a>
          ,{" "}
          <a href="https://www.linkedin.com/in/jack-peplinski/">
            Jack Peplinski
          </a>
        </div>
      </div>
    </div>
  );
}

export default App;
