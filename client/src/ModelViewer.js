import "./ScrewyDisplay.css";
import React, { Suspense } from "react";
import { Canvas } from "@react-three/fiber";
import { OrthographicCamera, OrbitControls, Stage ,PresentationControls} from "@react-three/drei";
import GltfModel from "./GltfModel";

const ModelViewer = ({ modelPath, scale = scale, position = [0, 0, 0] }) => {
    return (
      <Canvas dpr={[1,2]} style={{"position": "absolute"}}  className='rs'>
        <ambientLight intensity={20} />
        <spotLight position={[10, 10, 10]} angle={0.45} penumbra={1} />
        <pointLight position={[-10, -10, -10]} />
        <Suspense fallback={null}>
          <Stage environment={"night"}  background blur={5}/>
          <GltfModel  modelPath={modelPath} scale={scale} position={position} />
          <OrbitControls minZoom={4} maxZoom={20}/>
          <OrthographicCamera makeDefault
        zoom={1}
        top={230}
        bottom={-200}
        near={1}
        far={2000}
        position={[0, 0, 200]} />
        </Suspense>
      </Canvas>
    );
  };

export default ModelViewer;