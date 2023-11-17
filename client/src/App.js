import React,{useRef, useEffect, useState} from 'react';
import './App.css';


// import Navbar from './Navbar';
// import ScrewyDisplay from './ScrewyDisplay';
import ModelViewer from './ModelViewer';

function App() {
  
  return (
    <div className="App">
     {/* <Navbar/>
     <ScrewyDisplay/> */}
     <ModelViewer/>
    </div>
  );
}

export default App;
