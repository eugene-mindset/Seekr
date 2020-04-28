import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import { usePromiseTracker } from "react-promise-tracker";
import Spinner from 'react-bootstrap/Spinner'

const LoadingIndicator = props => {
  const { promiseInProgress } = usePromiseTracker();
  return (
    promiseInProgress &&
    <div 
    style={{
            marginTop: "100px",
            marginLeft: "50px",
            width: "100%",
            height: "100",
            display: "flex",
            justifyContent: "center",
            alignItems: "center"
           }}
    >
      <Spinner animation="border" role="status">
        <span className="sr-only">Loading...</span>
      </Spinner>
    </div>
  );  
}

ReactDOM.render(
  <div>
    <App />
    <LoadingIndicator/>
  </div>,
  document.getElementById('root')
);
