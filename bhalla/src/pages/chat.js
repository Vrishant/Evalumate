import React, { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { Container, Row, Col, Button, Form, InputGroup } from "react-bootstrap";
import { FileEarmarkText, Send } from "react-bootstrap-icons";

function App() {
  const [files, setFiles] = useState([]);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleFileUpload = (event) => {
    const uploadedFiles = Array.from(event.target.files);
    setFiles([...files, ...uploadedFiles]);
  };

  const handleSendMessage = () => {
    if (input.trim()) {
      setMessages([...messages, { sender: "User", text: input }]);
      setInput("");
      // Simulate bot response
      setTimeout(() => {
        setMessages((prev) => [...prev, { sender: "Bot", text: "This is a bot response." }]);
      }, 1000);
    }
  };

  return (
    <Container fluid className="bg-dark text-white vh-100">
      <Row>
        {/* Sidebar */}
        <Col md={3} className="bg-secondary vh-100 p-3 border-end border-light">
          <h4>Notebook</h4>
          <hr className="border-light" />
          <Button variant="dark" className="w-100 mb-2 text-white">
            <FileEarmarkText className="me-2" /> New Note
          </Button>
          <Form.Group>
            <Form.Label>Upload Documents</Form.Label>
            <Form.Control type="file" multiple onChange={handleFileUpload} className="bg-dark text-white" />
          </Form.Group>
          <ul className="mt-3">
            {files.map((file, index) => (
              <li key={index}>{file.name}</li>
            ))}
          </ul>
        </Col>

        {/* Main Chatbot System */}
        <Col md={9} className="p-4 d-flex flex-column h-100">
          <h3>Chatbot</h3>
          <div className="flex-grow-1 overflow-auto border p-3 bg-secondary rounded" style={{ height: "70vh" }}>
            {messages.map((msg, index) => (
              <div key={index} className={`mb-2 text-${msg.sender === "User" ? "end" : "start"}`}>
                <strong>{msg.sender}:</strong> {msg.text}
              </div>
            ))}
          </div>
          <InputGroup className="mt-3">
            <Form.Control
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type a message..."
              className="bg-dark text-white border-light"
            />
            <Button variant="light" onClick={handleSendMessage}>
              <Send />
            </Button>
          </InputGroup>
        </Col>
      </Row>
    </Container>
  );
}

export default App;
