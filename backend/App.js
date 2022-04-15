import React, { useState,useEffect,Component } from 'react';
import { Contacts } from "./components/Contacts";
import axios from 'axios'


class App extends Component {


  state = {
 
    // Initially, no file is selected
    selectedFile: null
  };
  
  // On file select (from the pop up)
  onFileChange = event => {
  
    // Update the state
    this.setState({ selectedFile: event.target.files[0] });
  
  };

  // On file upload (click the upload button)
  onFileUpload = () => {
      
    // Create an object of formData
    const formData = new FormData();

    // Update the formData object
    formData.append(
      'contacts',
      this.state.selectedFile,
      this.state.selectedFile.name
    );

    // Details of the uploaded file
    console.log(this.state.selectedFile);

    // Request made to the backend api
    // Send formData object
    axios.post('/load', formData);
  };




  /*data är variablen, setData är vad vi använder för att påverka den
  const [contacts,setData] = useState([{}]);
  useEffect(() => {
    fetch('/members').then(
      res => res.json() /* Hämta ifrån backend till json 
    ).then(
      data => {
        setData(data) /*setdata för att påverka variablen 
        console.log(contacts)
      }
    )
  }, []); /* tom array för att den enbart skall köras vid första laddnigen


  return (  
    <div className="App">
      <Contacts contacts={contacts}/>
      <input type="file" onChange={this.onFileChange} />
        <button onClick={this.onFileUpload}>Upload</button>
    </div>
 
  );
}*/

render() {
  return (
    <div>
        <h1>
          GeeksforGeeks
        </h1>
        <h3>
          File Upload using React!
        </h3>
        <div>
            <input type="file" onChange={this.onFileChange} />
            <button onClick={this.onFileUpload}>
              Upload!
            </button>
        </div>
      {this.fileData()}
    </div>
  );
}



}



export default App;