import { useEffect } from 'react';
import { useGLTF } from '@react-three/drei';

const ModelLoader = ({ url, onModelLoad }) => {
  const { scene } = useGLTF(url);
  
  useEffect(() => {
    onModelLoad(scene);
  }, [scene, onModelLoad]);

  return null;
};

export default ModelLoader;
