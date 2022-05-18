
import './App.css';
import ReactPlayer from 'react-player'


function App() {
  return (
    <div className="App">
      <ReactPlayer url='http://localhost:666/liveStream.m3u8' playing={true}  controls={true} muted />
      <ReactPlayer url='video/1.mp4' playing={true} controls={true} muted />
    </div>
  );
}

export default App;
