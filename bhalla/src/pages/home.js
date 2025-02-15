import React, { useState, useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { Container, Row, Col, Button, Nav } from "react-bootstrap";
import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import Particles from "../components/particles.js";
import GradientText from "../components/gradientText.js";
import Click from "../components/click.js";
import { Plus, Trash } from "react-bootstrap-icons";
import PixelCard from "../components/card.js";
import { v4 as uuidv4 } from 'uuid';
import Footer from "../components/footer.js";
import Navbar from "../components/navbar.js";

function Home() {
  const [notebooks, setNotebooks] = useState([]);

  useEffect(() => {
    const storedNotebooks = JSON.parse(localStorage.getItem("notebooks")) || [];
    setNotebooks(storedNotebooks);
  }, []);

  const addNotebook = () => {
    const newNotebook = {
      id: uuidv4(),
      title: `Notebook ${notebooks.length + 1}`,
      description: "New notebook",
    };
  
    const updatedNotebooks = [...notebooks, newNotebook];
    setNotebooks(updatedNotebooks);
    localStorage.setItem("notebooks", JSON.stringify(updatedNotebooks)); // Update localStorage immediately
  };
  

  const deleteNotebook = (id) => {
    const updatedNotebooks = notebooks.filter((notebook) => notebook.id !== id);
    setNotebooks(updatedNotebooks);
    localStorage.setItem("notebooks", JSON.stringify(updatedNotebooks)); // Update localStorage immediately
  };
  

  useEffect(() => {
    const storedNotebooks = localStorage.getItem("notebooks");
    if (storedNotebooks) {
      setNotebooks(JSON.parse(storedNotebooks));
    }
  }, []);

  return (
    <Container fluid className="min-vh-100 d-flex flex-column" style={{ backgroundColor: "#000000", color: "#FFFFFF", fontFamily: "Rasa, sans-serif" }}>
      <div style={{ position: 'sticky', top: 0, zIndex: 100 }}>
        <Navbar username="JohnDoe" />
      </div>
      <Click
        sparkColor='#fff'
        sparkSize={10}
        sparkRadius={15}
        sparkCount={8}
        duration={400}
      />
      <Row className="flex-grow-1">
        <Col className="p-4 d-flex flex-column animate__animated animate__fadeInRight" style={{ position: "relative" }}>
          <div style={{ position: "absolute", top: 0, left: 0, width: "100%", height: "100%", zIndex: 0 }}>
            <Particles 
              particleCount={900}
              particleSpread={2}
              speed={0.1}
              particleColors={["#2BC6D1", "#28007B", "#FFFFFF"]}
              moveParticlesOnHover={true}
              particleHoverFactor={1.2}
              alphaParticles={true}
              particleBaseSize={50}
              sizeRandomness={0.5}
              cameraDistance={15}
              disableRotation={false}
            />
          </div>
          
          <motion.div 
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-center"
            style={{ 
              position: "relative",
              zIndex: 1,
              marginTop: "10vh"
            }}
          >
            <h1 className="cube-logo" style={{ color: "#2BC6D1", fontSize: "6rem", fontWeight: "bolder", textShadow: "0px 0px 10px rgba(0, 0,0, 0.5)", textAlign: "center" }}>
              <GradientText
                colors={["#2BC6D1", "#2BC6D1", "#2BC6D1", "#28007B", "#2BC6D1"]}
                animationSpeed={8}
                showBorder={false}
                className="custom-class"
              >
                Welcome To The Future
              </GradientText>
            </h1>
          </motion.div>

          {/* <h2 className="mt-5" style={{ color: "#2BC6D1", fontSize: "3rem", fontWeight: "bold", textAlign: "left" }}>Your Notebooks</h2>
          <Button variant="primary" onClick={addNotebook} style={{ position: "relative", backgroundColor: "#2BC6D1", border: "none", borderRadius: "50%", width: "50px", height: "50px", fontSize: "24px", zIndex: 10 }}>
        <Plus />
      </Button> */}
              <div className="d-flex align-items-center mt-5">
                <h2 style={{ color: "#2BC6D1", fontSize: "3rem", fontWeight: "bold", textAlign: "left", marginRight: "15px" }}>Your Notebooks</h2>
                <Button variant="primary" onClick={addNotebook} style={{ position: "relative", backgroundColor: "#2BC6D1", border: "none", borderRadius: "50%", width: "50px", height: "50px", fontSize: "24px", zIndex: 10 }}>
                <Plus />
              </Button>
              </div>
          <hr style={{ border: "1px solid #FFFFFF", marginTop: "2px", width: "22%" }} />
          
          <Row className="mt-4 justify-content-center" style={{ minHeight: "100vh" }}>
            {notebooks.map((notebook) => (
              <Col key={notebook.id} md={3} className="mb-4">
                <motion.div
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <Link to={`/chat?id=${notebook.id}`} style={{ textDecoration: "none" }}>
                    <PixelCard variant="pink" style={{ boxShadow: "0px 0px 15px rgba(255, 255, 255, 0.5)", border: "3px solid #FFFFFF", padding: "20px", borderRadius: "10px"}}>
                      <div style={{ position: "absolute", top: "10px", left: "10px", right: "10px", bottom: "10px", display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center", color: "#FFFFFF",backdropFilter: 'blur(3px)', background: "transparent" }}>
                        <h3 style={{ color: "#2BC6D1", fontWeight: "bold" }}>{notebook.title}</h3>
                        <p style={{ textAlign: "center", fontSize: "1rem" }}>{notebook.description}</p>
                        <Button variant="danger" size="sm" style={{ position: "absolute", top: "10px", right: "10px" }} onClick={(e) => { e.preventDefault(); deleteNotebook(notebook.id); }}>
                          <Trash size={15} />
                        </Button>
                      </div>
                    </PixelCard>
                  </Link>
                </motion.div>
              </Col>
            ))}
          </Row>
        </Col>
      </Row>
      <Footer />
    </Container>
  );
}

export default Home;
