import "./ScrewyDisplay.css";
import axios from 'axios';
import React,{useRef, useEffect, useState} from 'react';


const ScrewyDisplay = () => {


  //usestate for camera status
  const [isCheckOn, setIsCheckOn] = useState('off');
  
  const statusData = {status : isCheckOn};

  const isPylonOn = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/publish');
      console.log( response.data)
    } catch (error) {
      console.error('Error fetching data:', error);
    }
/*
    try {
      const response_status = await axios.get('http://127.0.0.1:5000/get_status');
      setIsCheckOn(response_status.data['status']);
      console.log( response_status.data)
    } catch (error) {
      console.error('Error fetching data:', error);
    }
    
    if (setIsCheckOn == 'on' && isCheckOn == 'off') {
      //openPylonbutton
      alert('The device is ready');
    } else if (isCheckOn == 'on'){
      //closePylonbutton
      alert('The device is now closed');
    } else {
      alert('You have not connect to the device');
    };
  };
*/
  };
  //usestate for taking photo 
   const [dataPic, setdataPic] = useState({dataPic:[]});
   const takingPic = async () => {

   }; 
  
  //confirm
  const [usePic, setusePic] = useState(false);
  const confirmPic = async () => {

  };

  //retake
  function reTake() {

  };

  // use state to exporting to 
  const [data3D, setData3D] = useState({data3D: []});
  const [isSendType, setIsSendType] = useState(false);
  const [isLoading3D, setIsLoading3D] = useState(false);
  const [err, setErr] = useState('');

  // Add a function for exportButton to send the POST request ans get GET request
  const exportClick = async () => {
    setIsSendType(true);
    // Get the user selections from the dropdowns
    const selectedHead = document.querySelector(".head-select select");
    const selectedBit = document.querySelector(".bit-select select");

    console.log('selection is sending')
    // Create an object with the user selections
    const requestData = {
      type_head: selectedHead.options[selectedHead.selectedIndex].text,
      type_bit: selectedBit.options[selectedBit.selectedIndex].text,
    };
    // Send a POST request to the backend
    axios
      .post("http://127.0.0.1:5000/combine_and_store_data", requestData)
      .then((response) => {
        // Handle the response from the server
        console.log("Response from server:", response.data);
        setIsSendType(false);
      })
      .catch((error) => {
        // Handle any errors that occur during the request
        console.error("Error:", error);
        setIsSendType(false);
      });
    };

  return (
    <div className="plugin-file-cover-1">
      <div className="frame-parent">
        <div className="frame-child" />
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"/>
      </div>
      <div className="aboutUs">About Us</div>
      <div className="choosePicture" />
      <div className="show3D"> 
        <button className="clicksee">click here to see 3D model result</button>
      </div>
      <div className="toImage">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"/>
        <button className="checkOn" onClick={isPylonOn} ></button>
        <button className="takePhoto" onClick={takingPic} ><i className="fa fa-camera fa-2x" aria-hidden="true"></i></button>
        <button className="confirmImage" onClick={confirmPic}></button>
        <button className="retakePhoto" onClick={reTake} ></button>
      </div>
      <div className="showScrewInfo" >
        <div className="identifyTo">Screw Identifier</div>
        <div className="convertingTo">Converting 2D to 3D</div>
      </div>
      <div className="dimension">
        <div className= "nom"></div>
        <div className = "h"></div>
        <div className = "k"></div>
        <div className = "l"></div>
        <div className = "tl"></div>
        <div className = "sl"></div>
      </div>
      <div className="load">
        <button className="exportingTo" onClick={exportClick} >Export to 3D model</button>
      </div>
      <div className="loadTol">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"></link>
        <b className="clickto">click below to download</b>
        <a className="Download" href="https://www.w3schools.com" target="_blank"><i className="fa fa-download"></i> Download</a>
      </div>
      
      <div className="custom-select-frame">
        <div className="head-select" style = {{width: "100px"}}>
                <select>
                    <option value="0">Select head:</option>
                    <option value="1">HEX</option>
                    <option value="2">CAP</option>
                    <option value="3">DOME</option>
                    <option value="4">PAN</option>
                    <option value="5">COUNTER SINK</option>
                </select>
        </div>
        <div className="bit-select" style = {{width: "100px"}}>
            <select>
                    <option value="0">Select bit type:</option>
                    <option value="1">NONE</option>
                    <option value="2">ALLEN</option>
                    <option value="3">TORX</option>
                    <option value="4">PHILLIPS</option>
            </select>
        </div>
      </div> 
      <div className="text-select-frame">
        <div className ="HeadType">Head Type</div>
        <div className ="BitType">Bit Type</div>
      </div>
      <div className="text-result-frame">
        <div className ="size">Nominal Size</div>
        <div className ="headDia">Head Diameter (H) </div>
        <div className ="headHeight">Height of Head (K) </div>
        <div className ="blen">Bolt Length</div>
        <div className ="tlen">Thread Length</div>
        <div className ="slen">Space Length</div>
      </div>
    </div>
  );
};


export default ScrewyDisplay;
