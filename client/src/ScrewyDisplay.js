import "./ScrewyDisplay.css";
import React, { useRef, useState } from 'react';
import ModelViewer from './ModelViewer';
import image from './pinbg.jpg';

const ScrewyDisplay = () => {
  // use state for camera status
  const [isCheckOn, setIsCheckOn] = useState('off');

  const isPylonOn = async () => {
    try {
      // Send POST request using fetch
      await fetch("http://127.0.0.1:5000/publish", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ msg: 'isOn' }),
      });

      // Send GET request using fetch
      const response_status = await fetch('http://127.0.0.1:5000/get_status');
      const status_next = (await response_status.json()).msg;
      console.log(status_next);
      setIsCheckOn(status_next);
    } catch (error) {
      console.error('Error:', error);
    }

    if (isCheckOn === 'on') {
      alert('The device is ready');
    } else if (isCheckOn === 'off') {
      alert('The device is now closed');
    } else {
      alert('You have not connected to the device');
    }
  };

  // use state for taking photo
  const [dataPic, setdataPic] = useState({});
  const [showscrew2d, setshowscrew2d] = useState(false);

  const takingPic = async () => {
    setshowscrew2d(true);

    try {
      // Send POST request using fetch
      await fetch("http://127.0.0.1:5000/publish", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ msg: 'isTaken' }),
      });

      // Send GET request using fetch
      const response_pic = await fetch('http://127.0.0.1:5000/get_recent_captured_photo');
      const responseData = await response_pic.json();

      if (responseData && responseData.img_binary) {
        const base64Image = responseData.img_binary;
        setdataPic(base64Image);
      } else {
        throw new Error('Invalid response from the server');
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  // confirm picture to processed
  const [choosedScrew2d, setChoosedScrew2d] = useState(false);

  const [dataNom, setdataNom] = useState('');
  const [dataH, setdataH] = useState('');
  const [dataK, setdataK] = useState('');
  const [dataTL, setdataTL] = useState('');
  const [dataSL, setdataSL] = useState('');

  const confirmPic = async () => {
    setChoosedScrew2d(true);

    try {
      // Send POST request using fetch
      await fetch("http://127.0.0.1:5000/publish", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ msg: 'isProcessed' }),
      });

      // Send GET request using fetch
      const response_processing = await fetch('http://127.0.0.1:5000/get_processing');
      const dataresult = await response_processing.json();

      setdataNom(dataresult['M_Size']);
      setdataH(dataresult['Head_Diameter']);
      setdataK(dataresult['Head_Length']);
      setdataTL(dataresult['Thread_Length']);
      setdataSL(dataresult['Space_Length']);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  // retake photo - clear all information
  function reTake() {
    setshowscrew2d(false);
    setChoosedScrew2d(false);
    setshowdownload3D(current => false)
    setdataPic('');
    setdataNom('');
    setdataH('');
    setdataK('');
    setdataTL('');
    setdataSL('');
  }

  // use state to exporting to 
  const [data3D, setData3D] = useState('');
  const [isloading3D, setloading3D] = useState(false);
  const [showdownload3D,setshowdownload3D] = useState(false);
  
  const [err, setErr] = useState('');
  
  // Add a function for exportButton to send the POST request and get GET request
  const exportClick = async () => {

    setshowdownload3D(current => true)
    setloading3D(true)
    try {
      // Get the user selections from the dropdowns
      const selectedHead = document.querySelector(".head-select select");
      const selectedBit = document.querySelector(".bit-select select");
  
      // Create an object with the user selections
      const requestData = {
        type_head: selectedHead.options[selectedHead.selectedIndex].text,
        type_bit: selectedBit.options[selectedBit.selectedIndex].text,
      };
  
      // Send POST request using fetch
      await fetch("http://127.0.0.1:5000/combine_and_store_data", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
      });
  
      // Send GET request using fetch
      const response_glink = await fetch('http://127.0.0.1:5000/get_GoogleLink');
      const responseData = await response_glink.json();
      console.log('get_data', responseData);
      setData3D(responseData.link);
      setloading3D(false)
    } catch (error) {
      console.error('Error:', error);
      setErr('An error occurred while processing your request');
    }
  };

    //click see result process
    const screwy_3d = document.querySelector(".three_d");
    const [showscrew3d, setshowscrew3d] = useState(false);
    const Showscrew3d = event => {
       setshowscrew3d(current => !current);
    }
    

  return (
    <div className="plugin-file-cover-1" >
      <div className="frame-parent">
        <div className="frame-child" >
        {choosedScrew2d && (<img className= 'showphoto2' src={`data:image/jpeg;base64, ${dataPic}`} alt=""/>)}
        </div>
      </div>
      <div className="aboutUs">
        <b></b>
      </div>
      <div className="choosePicture" >
        {showscrew2d && (<img className= 'showphoto' src={`data:image/jpeg;base64, ${dataPic}`} alt=""/>)}
      </div>  
      <div className="show3D"> 
        <button className="clicksee" onClick={Showscrew3d}>show 3D model</button>
        {showscrew3d && (
         <ModelViewer  scale={0.1} modelPath={'../temp/downloaded.glb'} className='three_d' />
      )}
      </div> 
      <div className="toImage">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"/>
        <button className="checkOn" onClick={isPylonOn} ><i className="fa fa-power-off fa-2x" aria-hidden="true"></i></button>
        <button className="takePhoto" onClick={takingPic} ><i className="fa fa-camera fa-2x" aria-hidden="true"></i></button>
        <button className="confirmImage" onClick={confirmPic}><i className="fa fa-check-circle fa-2x" aria-hidden="true"></i></button>
        <button className="retakePhoto" onClick={reTake} ><i className="fa fa-times-circle fa-2x" aria-hidden="true"></i></button>
      </div>
      <div className="showScrewInfo" >
        <div className="identifyTo">Screw Identifier</div>
        <div className="convertingTo">Converting 2D to 3D</div>
      </div>
      <div className="dimension"> 
        <div className= "nom">{ choosedScrew2d && (<b>M {dataNom}</b>)}</div>
        <div className = "h">{ choosedScrew2d && (<b>{dataH} mm.</b>)}</div>
        <div className = "k">{ choosedScrew2d && (<b>{dataK} mm.</b>)}</div>
        <div className = "tl">{ choosedScrew2d && (<b>{dataTL} mm.</b>)}</div>
        <div className = "sl">{ choosedScrew2d && (<b>{dataSL} mm.</b>)}</div>
      </div>
      <div className="load">
        <button className="exportingTo" onClick={exportClick} >Export to 3D model</button>
      </div>
      <div className="loadTol">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"/>
        { showdownload3D && ( isloading3D ? (<i id='loady' className="fa fa-refresh fa-spin"></i>) :
        (
        <div>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"></link>
                <b className="clickto">click below to download</b>
                <a className="Download" target="_blank" href={data3D} ><i className="fa fa-download"></i> Download</a>
        </div> 
        ))}
      </div>
      
      <div className="custom-select-frame">
        <link href='https://fonts.googleapis.com/css?family=Alef' rel='stylesheet'/>
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
        <div className ="tlen">Thread Length</div>
        <div className ="slen">Grid Length</div>
      </div>
    </div>
   
  );
};


export default ScrewyDisplay;

//       <div className = "l">{ choosedScrew2d && (<b>{dataL} mm.</b>)}</div>
//        <div className ="blen">Bolt Length</div>
//  <div> className='picbg'style={{ backgroundImage:`url(${image})` ,backgroundRepeat:"no-repeat"}}</div>


