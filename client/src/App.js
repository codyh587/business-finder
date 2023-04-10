import { BrowserRouter, Routes, Route } from 'react-router-dom'
import CreateMap from "./pages/CreateMap";
import UpdateMap from "./pages/UpdateMap";
import ViewMap from "./pages/ViewMap";
import "./style.css"

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<CreateMap />} />
          <Route path="/viewMap/:id" element={<ViewMap />} />
          <Route path="/updateMap/:id" element={<UpdateMap />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
