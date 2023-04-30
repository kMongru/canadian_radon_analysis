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
    const test = Papa.parse(files, {
      header: true,
      skipEmptyLines: true,
      complete: function (results) {
        console.log(results.data);
      },
    });
    // const resp = await (await fetch(`/api/`)).json();

    setTimeout(() => {
      setStatus("results");
    }, 5000);

    setResults(test);
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
      return <p>results</p>;
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
          Julia Groza, Rhys Dominguez, Keegan Mongru, Cullen Macleod, Jack
          Peplinski
        </div>
      </div>
    </div>
  );
}

export default App;