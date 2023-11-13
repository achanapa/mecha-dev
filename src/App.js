import React,{useState} from 'react';
import './App.css';

import Navbar from './Navbar';
import PluginFileCover1 from './plugin';
let id=1; 

function App() {
  const [posts,setPosts] = useState([]);

  function addPost(title){
    const newPost = {id,title:title};
    setPosts([newPost, ...posts]);
    id += 1;
  }
  return (
    <div className="App">
     <Navbar />
     <PluginFileCover1/>

    </div>
  );
}

export default App;
