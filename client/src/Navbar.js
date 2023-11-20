import React from 'react' ; 
import axios from 'axios';

const Navbar = () => {
    
    function topFunction() {
    document.body.scrollTop = 70; 
    document.documentElement.scrollTop = 70;
    };

    function perfFunction() {
    document.body.scrollTop = 1000; 
    document.documentElement.scrollTop = 1000;
    };

    function aboutFunction() {
    document.body.scrollTop = 1800; 
    document.documentElement.scrollTop = 1800;
    };
 
    return(
    <header className="Navbar">
    <header className="Navg"></header>
    <b className="screwyio">Screwy.io</b>
    <button className = "about" onClick = {aboutFunction} id = "aboutt">About</button>
    <button className="performance" onClick = {perfFunction}  id ="perff">Performance</button>
    <button  className="get-started-wrapper"  onClick = {topFunction}  id ="getit" >
         <b className="get-started">Get Started</b> 
     </button>
    </header>
    );
    
};


export default Navbar;
