import "./ScrewyDisplay.css";
import axios from 'axios';
import React,{ useRef,useEffect, useState} from 'react';
import ModelViewer from './ModelViewer';

const ScrewyDisplay = () => {

  //usestate for camera status
  const [isCheckOn, setIsCheckOn] = useState('off');
  const previousCheckOn = useRef("");

  useEffect(() => {
    previousCheckOn.current = isCheckOn;
  }, [isCheckOn]);


  const isPylonOn = async () => {
   
    axios
      .post("http://127.0.0.1:5000/publish", {msg:'isOn'})
      .then((response) => {
        // Handle the response from the server
        console.log("Response from server: done");
      })
      .catch((error) => {
        // Handle any errors that occur during the request
        console.error("Error:", error);
        setIsSendType(false);
      });
    
    try {
      const response_status = await axios.get('http://127.0.0.1:5000/get_status');
      setIsCheckOn(response_status.data['msg']);
      console.log(response_status.data)
    } catch (error) {
      console.error('Error fetching data:', error);
    }
    
    if ( isCheckOn == 'on') {
      //openPylonbutton
      alert('The device is ready');
    } else if (isCheckOn == 'off') {
      alert('You have not connect to the device');
    } else {
      //closePylonbutton
      alert('The device is now closed');
    };
  };

  //usestate for taking photo 
   const [dataPic, setdataPic] = useState('');
   const takingPic = async () => {
    axios
    .post("http://127.0.0.1:5000/publish", {msg:'isTaken'})
    .then((response_pic) => {
      // Handle the response from the server
      console.log("Picture from server is sent");
    })
    .catch((error) => {
      // Handle any errors that occur during the request
      console.error("Error:", error);
      setIsSendType(false);
    });

    try {
      const response_pic = await axios.get('http://127.0.0.1:5000/get_recent_captured_photo');

      if (response_pic.data && response_pic.data.img_binary) {
        const base64Image = response_pic.data.img_binary;
        setdataPic(base64Image);
      } else {
        throw new Error('Invalid response from the server');
      }

    } catch (error) {
      console.error('Error fetching data:', error);
    }

  };
  
  //confirm
  const [dataResult, setdataResult] = useState('');
  const [dataNom, setdataNom] = useState('');
  const [dataH, setdataH] = useState('');
  const [dataK, setdataK] = useState('');
  const [dataL, setdataL] = useState('');
  const [dataTL, setdataTL] = useState('');
  const [dataSL, setdataSL] = useState('');

  const confirmPic = async () => {
    axios
    .post("http://127.0.0.1:5000/publish", {msg:'isProcessed'})
    .then((response_result) => {
      // Handle the response from the server
      console.log("Processed image from server:", response_result.data);
    })
    .catch((error) => {
      // Handle any errors that occur during the request
      console.error("Error:", error);
      
    });

    try {
      const response_processing = await axios.get('http://127.0.0.1:5000/get_processing');
      console.log('get_data',response_processing.data);
      const dataresult = response_processing.data;
      setdataNom(dataresult['M_Size'])
      setdataH(dataresult['Head_Diameter'])
      setdataK(dataresult['Head_Length'])
      setdataTL(dataresult['Thread_Length'])
      setdataSL(dataresult['Space_Length'])
      //console.log(response_pic.data)
    } catch (error) {
      console.error('Error fetching data:', error);
    }
 
  };

  //retake
  function reTake() {
    setdataPic('')
    setdataNom('')
    setdataH('')
    setdataK('')
    setdataTL('')
    setdataSL('')

  };

  // use state to exporting to 
  const [data3D, setData3D] = useState({});
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
        setIsSendType(false);
      })
      .catch((error) => {
        // Handle any errors that occur during the request
        console.error("Error:", error);
        setIsSendType(false);
      });

    try {
        const response_glink = await axios.get('http://127.0.0.1:5000/get_GoogleLink');
        console.log('get_data',response_glink.data);
        setData3D(response_glink.data['link'])
      } catch (error) {
        console.error('Error fetching data:', error);
      }

    };

    //click see result process

    const screwy_3d = document.querySelector(".three_d");
    const [showscrew3d, setshowscrew3d] = useState(false);
    
    const Showscrew3d = event => {
       setshowscrew3d(current => !current);
    
      };
      

  return (
    <div className="plugin-file-cover-1">
      <div className="frame-parent">
        <div className="frame-child" />
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"/>
      </div>
      <div className="aboutUs">About Us</div>
      <div className="choosePicture" >
        <img className= 'showphoto' src={`data:image/jpeg;base64, ${dataPic}`} alt=""/>
      </div>  
      <div className="show3D"> 
        <button className="clicksee" onClick={Showscrew3d}>show 3D model</button>
        {showscrew3d && (
         <ModelViewer  scale={0.1} modelPath={'../Bolt_ID38.glb'} className='three_d' />
      )}
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
        <div className= "nom">M {dataNom} </div>
        <div className = "h">{dataH} mm.</div>
        <div className = "k">{dataK} mm.</div>
        <div className = "l">{dataL} mm.</div>
        <div className = "tl">{dataTL} mm.</div>
        <div className = "sl">{dataSL} mm.</div>
      </div>
      <div className="load">
        <button className="exportingTo" onClick={exportClick} >Export to 3D model</button>
      </div>
      <div className="loadTol">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"></link>
        <b className="clickto">click below to download</b>
        <a className="Download" href={data3D} target="_blank"><i className="fa fa-download"></i> Download</a>
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

