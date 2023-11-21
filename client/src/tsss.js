import { useLoader } from  "@react-three/fiber";
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader';



function Tese() {
    const gltf = useLoader(GLTFLoader, '../SciFiTram.glb');
    return <primitive object={gltf.scene} />;
  
};

export default Tese;