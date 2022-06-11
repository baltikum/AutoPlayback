
//import axios from 'axios'
//import React, { useState, useEffect } from 'react';

import React, { useState, useEffect }from 'react';

import './App.css';

import NavBar from './components/navbar/NavBar';
import { BrowserRouter as Router, Routes, Route, Navigate }
	from 'react-router-dom';


import Playback from './pages/Playback';
import Live from './pages/Live';
//import Recorded from './pages/Recorded';
import Settings from './pages/Settings';
import Login from './pages/Login';

import Protected from './components/Protected';

require('dotenv').config()


const LOCAL_STORAGE_KEY = 'AutoPlaybackApp.user'


function App() {




      const [loggedIn, setLoggedIn] = useState(false);
      const [loggedUser, setLoggedInUser ] = useState({})

      const [presence, setPresence] = useState(false);
//<Route exact path='/' element={<Playback />} />

      return (
      <>
            <Router>

                  <NavBar />

                  <Routes>
                        <Route exact path='/' element={
                              <Protected isLoggedIn={loggedIn} presence={presence}>
                                    <Playback />
                              </Protected>
                        } />
                        
                        <Route path='/live' element={<Live/>} />

                        <Route path='/settings' element={
                              <Protected isLoggedIn={loggedIn}>
                                    <Settings />
                              </Protected>
                        } />

                        <Route path='/login' element={
                              <Login 
                                    setLoggedIn={setLoggedIn}                                           
                                    setLoggedInUser={setLoggedInUser}        
                                    loginStatus={loggedIn}
                                    user={loggedUser} /> } />


                  </Routes>
                  
            </Router>
      </>
      );
      }

export default App;