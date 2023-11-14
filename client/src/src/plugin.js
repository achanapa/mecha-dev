import "./PluginFileCover1.css";

const PluginFileCover1 = () => {
  return (
    <div className="plugin-file-cover-1">
      <div className="frame-parent">
        <div className="frame-child" />
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"/>
      </div>
      <div className="aboutUs">About Us</div>
      <div className="plugin-file-cover-1-item" />
      <div className="plugin-file-cover-1-inner"> 
        <button className="clicksee">click here to see the result</button>
      </div>
      <div className="rectangle-group">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"/>
        <button className="group-child1" ></button>
        <button className="group-child2" ><i class="fa fa-camera fa-2x" aria-hidden="true"></i></button>
        <button className="group-child3" ></button>
        <button className="group-child4" ></button>
      </div>
      <div className="plugin-file-cover-1-child1" >
        <div className="identifyTo">Screw Identifier</div>
        <div className="convertingTo">Converting 2D to 3D</div>
        <div className="Result">Result</div>
      </div>
      <div className="result">
        <button className="done">Done</button>
      </div>
      <div className="dimension">
        <div className= "nom"></div>
        <div className = "h"></div>
        <div className = "k"></div>
        <div className = "l"></div>
      </div>
      <div className="load">
        <button className="exportingTo">Export to 3D model</button>
      </div>
      <div className="loadTol">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"></link>
        <b className="clickto">click below to download</b>
        <a className="Download" href="https://www.w3schools.com" target="_blank"><i class="fa fa-download"></i> Download</a>
      </div>
      
      <div className="custom-select-frame">
        <div className="head-select" style = {{width: "100px"}}>
                <select>
                    <option value="0">Select head:</option>
                    <option value="1">HEX</option>
                    <option value="2">CAP</option>
                    <option value="3">DOME</option>
                    <option value="4">PAN</option>
                    <option value="3">COUNTER SINK</option>
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
        <div className ="len">Length</div>
      </div>
    </div>
  );
};

export default PluginFileCover1;
