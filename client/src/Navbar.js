import React from 'react' ; 
import axios from 'axios';

const Navbar = () => {
    
    function topFunction() {
    document.body.scrollTop = 70; 
    document.documentElement.scrollTop = 70;
    };

    // test
    const reactData = { id: 1, 'name':' Tom'};
    const url = "http://127.0.0.1:5000/publish";
    const sendData = () => {
    axios.post(url, reactData)
        .then(res => console.log(reactData))
        .catch(err => console.log(err.data))
    };
 
    return(
    <header className="Navbar">
    <header className="Navg"></header>
    <button className='Test' onClick={sendData} >Test</button>
    <b className="screwyio">Screwy.io</b>
    <button className = "about" onClick = {topFunction} id = "aboutt">About</button>
    <button className="performance" onClick = {topFunction}  id ="perff">Performance</button>
    <button  className="get-started-wrapper"  onClick = {topFunction}  id ="getit" >
         <b className="get-started">Get Started</b> 
     </button>
    </header>
    );
    
};


export default Navbar;
