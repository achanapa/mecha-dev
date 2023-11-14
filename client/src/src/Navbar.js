import React from 'react' ; 


const Navbar = () => {
    
    function topFunction() {
    document.body.scrollTop = 70; 
    document.documentElement.scrollTop = 70;
    }
 
    return(
    <header className="Navbar">
    <header className="Navg"></header>
    <b className="screwyio">Screwy.io</b>
    <button className = "about" onClick = {topFunction} id = "aboutt">About</button>
    <button className="performance" onClick = {topFunction}  id ="perff">Performance</button>
    <button  class="get-started-wrapper"  onClick = {topFunction}  id ="getit" >
         <b className="get-started">Get Started</b> 
     </button>
    </header>
    );
    
};


export default Navbar;
