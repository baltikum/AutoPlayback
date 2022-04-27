
import React, { useEffect } from 'react';
import './App.css';

import NavBar from './components/navbar/NavBar';
import { BrowserRouter as Router, Routes, Route}
	from 'react-router-dom';

import Playback from './pages/Playback';
import Live from './pages/Live';
import Recorded from './pages/Recorded';
import Settings from './pages/Settings';
import Login from './pages/Login';

require('dotenv').config()

function App() {
      const [playbacks,setPlayback] = useState([])


      /* Fetches array with info about recordings files*/
      const fetchPlayback = async () => {
            axios.get('/playback/fetch').then(
                  (response) => {
                        setPlayback(response.data)
                        console.log(response.data);
                  },
                  (error) => {
                        console.log(error);
                  }
            ); 
      }
      useEffect(() => {
            fetchPlayback()
      },[]);





      return (
      <>
            <Router>

                  <NavBar />

                  <Routes>
                        <Route exact path='/' element={<Playback playbacks={playbacks} />} />
                        <Route path='/live' element={<Live />} />
                        <Route path='/recorded' element={<Recorded/>} />
                        <Route path='/settings' element={<Settings/>} />
                        <Route path='/login' element={<Login />} />
                  </Routes>
                  
            </Router>
      </>
      );
      }

export default App;