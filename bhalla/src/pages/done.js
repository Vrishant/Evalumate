import React, { useState, useRef, useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { Container, Row, Col, Form, InputGroup, Button, Alert } from "react-bootstrap";
import { Send, ChevronLeft, ChevronRight } from "react-bootstrap-icons";
import { motion } from "framer-motion";
import Particles from "../components/particles.js";

function App() {
  const [files, setFiles] = useState([]);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [uploadError, setUploadError] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const chatRef = useRef(null);

  const validFileTypes = ['application/pdf', 'text/plain', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
  const maxFileSize = 10 * 1024 * 1024; // 5MB

  const handleFileUpload = (event) => {
    const uploadedFiles = Array.from(event.target.files);
    setUploadError(null);
    setIsUploading(true);

    // Validate files
    const invalidFiles = uploadedFiles.filter(file => {
      return !validFileTypes.includes(file.type) || file.size > maxFileSize;
    });

    if (invalidFiles.length > 0) {
      setUploadError(`Invalid files detected. Please upload only PDF, TXT, or DOC files under 10MB.`);
      setIsUploading(false);
      return;
    }

    // Simulate file upload process
    setTimeout(() => {
      setFiles(prevFiles => [...prevFiles, ...uploadedFiles]);
      setIsUploading(false);
    }, 1000);
  };

  const handleSendMessage = () => {
    if (input.trim()) {
      setMessages([...messages, { sender: "User", text: input, timestamp: new Date().toLocaleTimeString() }]);
      setInput("");
      setTimeout(() => {
        setMessages((prev) => [...prev, { sender: "Bot", text: "This is a bot response.", timestamp: new Date().toLocaleTimeString() }]);
      }, 1000);
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <Container fluid className="vh-100 d-flex flex-column" style={{ backgroundColor: "#000000", color: "#FFFFFF", fontFamily: "Rasa, sans-serif" }}>
      <Row className="flex-grow-1">
        {sidebarOpen && (
          <Col md={3} className="vh-100 p-3 border-end d-flex flex-column animate__animated animate__fadeInLeft" style={{ backgroundColor: "#1A1A1A", color: "#FFFFFF", fontFamily: "Zen Dots, sans-serif", wordWrap: "break-word", position: "relative" }}>
            <Button variant="link" onClick={() => setSidebarOpen(false)} style={{ position: "fixed", top: "20px", left: "20%", color: "#2BC6D1", zIndex: 1000 }}>
              <ChevronLeft size={20} />
            </Button>
            <h4 style={{ color: "#2BC6D1", fontFamily: "Zen Dots, sans-serif", fontWeight: 'Bold' }}><em>Notebook</em></h4>
            <hr style={{ borderColor: "#2BC6D1" }} />
            <Form.Group>
              <Form.Label style={{ color: "#2BC6D1" }}>Upload Documents</Form.Label>
              <Form.Control 
                type="file" 
                multiple 
                onChange={handleFileUpload} 
                disabled={isUploading}
                style={{ backgroundColor: "#000000", color: "#FFFFFF", borderColor: "#2BC6D1", borderRadius: "10px" }} 
              />
              {isUploading && <div className="mt-2" style={{ color: "##2BC6D1" }}>Uploading files...</div>}
              {uploadError && <Alert variant="danger" className="mt-2">{uploadError}</Alert>}
            </Form.Group>
            <ul className="mt-3" style={{ listStyle: "none", padding: 0 }}>
              {files.length > 0 ? files.map((file, index) => (
                <li key={index} style={{ padding: "5px 0", color: "#2BC6D1", wordWrap: "break-word" }}>
                  {file.name}
                </li>
              )) : <li style={{ color: "#888" }}>No documents uploaded</li>}
            </ul>
          </Col>
        )}
        
        {!sidebarOpen && (
          <Button variant="link" onClick={() => setSidebarOpen(true)} style={{ position: "fixed", top: "20px", left: "", color: "#2BC6D1", zIndex: 1000 }}>
            <ChevronRight size={20} />
          </Button>
        )}

        <Col md={sidebarOpen ? 9 : 12} className="p-4 d-flex flex-column h-100 animate__animated animate__fadeInRight" style={{ borderRadius: "0 20px 20px 0", position: "relative", width: sidebarOpen ? "75%" : "100%" }}>
          <h3 style={{ color: "#2BC6D1", fontFamily: "Zen Dots, sans-serif" }}><em>Evalumate</em></h3>
          <div style={{ position: "absolute", top: 0, left: 0, width: "100%", height: "100%", zIndex: 0 }}>
            <Particles 
              particleCount={700}
              particleSpread={2}
              speed={0.3}
              particleColors={["#2BC6D1", "#28007B"]}
              moveParticlesOnHover={false}
              particleHoverFactor={2}
              alphaParticles={true}
              particleBaseSize={50}
              sizeRandomness={0.5}
              cameraDistance={15}
              disableRotation={false}
            />
          </div>
          <div ref={chatRef} className="flex-grow-1 overflow-auto p-4 rounded animate__animated animate__fadeIn" style={{ 
            backgroundColor: "rgba(26, 26, 26, 0.9)", 
            color: "#FFFFFF", 
            borderRadius: "20px",
            background: 'transparent', 
            backdropFilter: "blur(4px)", 
            position: "relative", 
            zIndex: 1,
            height: "calc(100vh - 200px)",
            marginBottom: "20px"
          }}>
            {messages.map((msg, index) => (
              <motion.div 
                key={index}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.3 }}
                style={{ 
                  display: "flex",
                  justifyContent: msg.sender === "User" ? "flex-end" : "flex-start",
                  marginBottom: "15px",
                }}
              >
                <div 
                  style={{ 
                    maxWidth: "80%",
                    padding: "14px 20px",
                    borderRadius: "25px",
                    fontSize: "18px",
                    color: msg.sender === "User" ? "#fff" : "#000",
                    background: msg.sender === "User" 
                      ? "linear-gradient(to right, #2BC6D1, #28007B)" 
                      : "linear-gradient(to right, #f1f1f1, #e0e0e0)",
                    boxShadow: "0px 4px 12px rgba(0, 0, 0, 0.3)",
                    position: "relative",
                  }}
                >
                  {msg.text}
                  <div style={{ fontSize: "12px", marginTop: "8px", textAlign: "right", opacity: 0.7 }}>
                    {msg.timestamp}
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
          <div className="p-3 mt-3 animate__animated animate__fadeInUp" style={{ backgroundColor: "#1A1A1A", borderRadius: "20px", position: "relative", zIndex: 1 }}>
            <InputGroup>
              <Form.Control
                as="textarea"
                rows={1}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyPress}
                placeholder="Type a message..."
                style={{ backgroundColor: "#000000", color: "#FFFFFF", borderColor: "#2BC6D1", borderRadius: "25px", fontFamily: "Oswald, sans-serif", fontSize: "16px", padding: "12px", resize: "none" }}
              />
              <Button style={{ backgroundColor: "#2BC6D1", color: "#000000", borderRadius: "15px", marginLeft: "3px" }} onClick={handleSendMessage}>
                <Send size={20} />
              </Button>
            </InputGroup>
          </div>
        </Col>
      </Row>
    </Container>
  );
}

export default App;
