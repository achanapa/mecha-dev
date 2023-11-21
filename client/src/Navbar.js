import React from 'react' ; 
import axios from 'axios';

const Navbar = () => {
    
    function topFunction() {
    document.body.scrollTop = 70; 
    document.documentElement.scrollTop = 70;
    };

<<<<<<< HEAD
    // test
    const reactData = { id: 1, 'name':' Tom'};
    const url = "http://127.0.0.1:5000/publish";
    const sendData = () => {
    axios.post(url, reactData)
        .then(res => console.log(reactData))
        .catch(err => console.log(err.data))
=======
    function perfFunction() {
    document.body.scrollTop = 1000; 
    document.documentElement.scrollTop = 1000;
    };

    function aboutFunction() {
    document.body.scrollTop = 1800; 
    document.documentElement.scrollTop = 1800;
>>>>>>> emer
    };
 
    return(
    <header className="Navbar">
    <header className="Navg"></header>
<<<<<<< HEAD
    <button className='Test' onClick={sendData} >Test</button>
    <b className="screwyio">Screwy.io</b>
    <button className = "about" onClick = {topFunction} id = "aboutt">About</button>
    <button className="performance" onClick = {topFunction}  id ="perff">Performance</button>
=======
    <b className="screwyio">Screwy.io</b>
    <button className = "about" onClick = {aboutFunction} id = "aboutt">About</button>
    <button className="performance" onClick = {perfFunction}  id ="perff">Performance</button>
>>>>>>> emer
    <button  className="get-started-wrapper"  onClick = {topFunction}  id ="getit" >
         <b className="get-started">Get Started</b> 
     </button>
    </header>
    );
    
};


export default Navbar;
