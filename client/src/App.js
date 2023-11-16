import React,{useRef, useEffect, useState} from 'react';
import './App.css';


import Navbar from './Navbar';
import ScrewyDisplay from './ScrewyDisplay';

function App() {
  
  return (
    <div className="App">
     <Navbar/>
     <ScrewyDisplay/>
    </div>
  );
}

export default App;
