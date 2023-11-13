import "./PluginFileCover1.css";

const PluginFileCover1 = () => {
  return (
    <div className="plugin-file-cover-1">
      <div className="frame-parent">
        <div className="frame-child" />
        <div className="frame-child" />
        <div className="frame-child" />
      </div>

      <div className="plugin-file-cover-1-item" />
      <div className="plugin-file-cover-1-inner" />
      <div className="rectangle-group">
        <button className="group-child1" ></button>
        <button className="group-child2" ></button>
        <button className="group-child3" ></button>
        <button className="group-child4" ></button>
      </div>
      <div className="plugin-file-cover-1-child1" >
        <div className="convertingTo">Converting 2D to 3D</div>
        <button className="exportingTo">Export to 3D model</button>
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

    </div>
  );
};

export default PluginFileCover1;
