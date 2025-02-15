import React, { useState, useRef, useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { Container, Row, Col, Form, InputGroup, Button, Alert } from "react-bootstrap";
import { Send, ChevronLeft, ChevronRight } from "react-bootstrap-icons";
import { motion } from "framer-motion";
import Particles from "../components/particles";
import GradientText from "../components/gradientText";
import Navbar from "../components/navbar";
import Footer from "../components/footer";

function Chat() {
  const [files, setFiles] = useState([]);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [uploadError, setUploadError] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const chatRef = useRef(null);

  const validFileTypes = ['application/pdf', 'text/plain', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
  const maxFileSize = 10 * 1024 * 1024; 

  const handleFileUpload = (event) => {
    const uploadedFiles = Array.from(event.target.files);
    setUploadError(null);
    setIsUploading(true);

    const invalidFiles = uploadedFiles.filter(file => {
      return !validFileTypes.includes(file.type) || file.size > maxFileSize;
    });

    if (invalidFiles.length > 0) {
      setUploadError(`Invalid files detected. Please upload only PDF, TXT, or DOC files under 10MB.`);
      setIsUploading(false);
      return;
    }

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
    <Container fluid className="min-vh-100 d-flex flex-column" style={{ backgroundColor: "#000000", color: "#FFFFFF", fontFamily: "Rasa, sans-serif" }}>
       <div style={{ position: 'sticky', top: 0, zIndex: 100 }}>
        <Navbar username="JohnDoe" />
      </div>
      <Row className="flex-grow-1" style={{ position: 'relative' }}>
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

        {sidebarOpen && (
          <Col md={3} className="p-3 d-flex flex-column" style={{ backgroundColor: "rgba(26, 26, 26, 0.9)", backdropFilter: "blur(5px)", position: "relative", zIndex: 1 }}>
            <h4 style={{ color: "#2BC6D1", fontWeight: "bold" }}>
              <GradientText
                colors={["#2BC6D1", "#2BC6D1", "#2BC6D1", "#28007B", "#2BC6D1"]}
                animationSpeed={8}
                showBorder={false}
              >
                Notebook
              </GradientText>
            </h4>
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
              {isUploading && <div className="mt-2" style={{ color: "#2BC6D1" }}>Uploading files...</div>}
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

        <Col md={sidebarOpen ? 9 : 12} className="p-4 d-flex flex-column" style={{ position: "relative", zIndex: 1 }}>
          <h3 style={{ color: "#2BC6D1", fontWeight: "bold" }}>
            <GradientText
              colors={["#2BC6D1", "#2BC6D1", "#2BC6D1", "#28007B", "#2BC6D1"]}
              animationSpeed={8}
              showBorder={false}
            >
              Evalumate
            </GradientText>
          </h3>
          <div ref={chatRef} className="flex-grow-1 overflow-auto p-4 rounded" style={{ 
              backgroundColor: "rgba(26, 26, 26, 0.9)", 
              backdropFilter: "blur(5px)", 
              borderRadius: "20px",
              marginBottom: "20px",
              minHeight: "70vh",  // Increase the chat area height
              maxHeight: "80vh"   // Optional: Limit max height to prevent overflow
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
          <div className="p-3 rounded" style={{ backgroundColor: "rgba(26, 26, 26, 0.9)", backdropFilter: "blur(5px)", borderRadius: "20px" }}>
            <InputGroup>
              <Form.Control
                as="textarea"
                rows={1}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyPress}
                placeholder="Type a message..."
                style={{ backgroundColor: "#000000", color: "#FFFFFF", borderColor: "#2BC6D1", borderRadius: "25px", fontSize: "16px", padding: "12px", resize: "none" }}
              />
              <Button style={{ backgroundColor: "#2BC6D1", color: "#000000", borderRadius: "15px", marginLeft: "3px" }} onClick={handleSendMessage}>
                <Send size={20} />
              </Button>
            </InputGroup>
          </div>
        </Col>
      </Row>
      <Footer />
    </Container>
  );
}

export default Chat;
