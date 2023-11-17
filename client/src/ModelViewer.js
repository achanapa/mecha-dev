import React, { useRef, Suspense } from 'react';
import { Canvas } from "@react-three/fiber";
import ModelLoader from './ModelLoader'

const ModelViewer = () => {
  const modelRef = useRef();

  const onModelLoad = (gltf) => {
    modelRef.current = gltf.scene;
  };

  return (
    <Canvas>
      <ambientLight />
      <directionalLight position={[10, 10, 10]} />
      <pointLight position={[-10, -10, -10]} />
      <group ref={modelRef} />
      <mesh visible position={[0, 0, 0]} rotation={[0, 0, 0]} onPointerOver={(e) => e.stopPropagation()}>
        <boxBufferGeometry attach="geometry" args={[1, 1, 1]} />
        <meshStandardMaterial attach="material" color="blue" />
      </mesh>
      <Suspense fallback={null}>
        <mesh>
          <primitive object={modelRef.current} />
          <meshStandardMaterial color="red" />
        </mesh>
        <ModelLoader url="../backend/temp/downloaded.glb" onModelLoad={onModelLoad} />
      </Suspense>
    </Canvas>
  );
};

export default ModelViewer;
