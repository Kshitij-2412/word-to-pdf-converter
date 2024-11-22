import React, { useState } from 'react';
import axios from 'axios';
import {
  Box,
  Button,
  Card,
  CardContent,
  CircularProgress,
  Container,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  IconButton,
  LinearProgress,
  Paper,
  Snackbar,
  Stack,
  TextField,
  Typography,
  Alert,
} from '@mui/material';
import { styled } from '@mui/material/styles';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import LockIcon from '@mui/icons-material/Lock';
import DownloadIcon from '@mui/icons-material/Download';
import DeleteIcon from '@mui/icons-material/Delete';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import { API_URL } from './config';

// Styled components
const VisuallyHiddenInput = styled('input')({
  clip: 'rect(0 0 0 0)',
  clipPath: 'inset(50%)',
  height: 1,
  overflow: 'hidden',
  position: 'absolute',
  bottom: 0,
  left: 0,
  whiteSpace: 'nowrap',
  width: 1,
});

const MetadataCard = styled(Card)(({ theme }) => ({
  marginTop: theme.spacing(2),
  marginBottom: theme.spacing(2),
  backgroundColor: '#f8f9fa',
  boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  transition: 'transform 0.2s ease-in-out',
  '&:hover': {
    transform: 'translateY(-2px)',
    boxShadow: '0 4px 8px rgba(0,0,0,0.15)',
  },
}));

const MetadataItem = styled(Box)(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  marginBottom: theme.spacing(1),
  padding: theme.spacing(1),
  borderRadius: theme.shape.borderRadius,
  backgroundColor: 'white',
  '&:last-child': {
    marginBottom: 0,
  },
}));

const MetadataLabel = styled(Typography)(({ theme }) => ({
  fontWeight: 600,
  minWidth: '120px',
  color: theme.palette.text.secondary,
}));

const MetadataValue = styled(Typography)(({ theme }) => ({
  color: theme.palette.text.primary,
  wordBreak: 'break-word',
}));

function App() {
  const [file, setFile] = useState(null);
  const [metadata, setMetadata] = useState(null);
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [showPasswordDialog, setShowPasswordDialog] = useState(false);
  const [isDragActive, setIsDragActive] = useState(false);

  const formatBytes = (bytes) => {
    if (!bytes || isNaN(bytes)) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDate = (dateString) => {
    if (!dateString) return '';
    try {
      const date = new Date(dateString);
      return date.toLocaleString();
    } catch (e) {
      return '';
    }
  };

  const handleDragEnter = (e) => {
    e.preventDefault();
    setIsDragActive(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragActive(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragActive(false);
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.name.endsWith('.docx')) {
      setFile(droppedFile);
      handleUpload(droppedFile);
    } else {
      setError('Please upload a .docx file');
    }
  };

  const handleFileSelect = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      handleUpload(selectedFile);
    }
  };

  const handleUpload = async (selectedFile) => {
    try {
      setLoading(true);
      setError(null);
      setMetadata(null);
      setUploadProgress(0);

      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await axios.post(`${API_URL}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          setUploadProgress(progress);
        },
      });

      setMetadata(response.data.metadata);
      setSuccess('File uploaded successfully');
      setShowPasswordDialog(true);
    } catch (err) {
      console.error('Upload error:', err);
      setError(err.response?.data?.error || 'Upload failed');
    } finally {
      setLoading(false);
    }
  };

  const handleConvert = async () => {
    try {
      setLoading(true);
      setError(null);

      const formData = new FormData();
      formData.append('file', file);
      if (password) {
        formData.append('password', password);
      }

      const response = await axios.post(`${API_URL}/convert`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const downloadUrl = `${API_URL}/download/${response.data.filename}`;
      window.location.href = downloadUrl;
      
      setSuccess('File converted successfully');
      setShowPasswordDialog(false);
      setPassword('');
    } catch (err) {
      console.error('Conversion error:', err);
      setError(err.response?.data?.error || 'Conversion failed');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFile(null);
    setMetadata(null);
    setPassword('');
    setError(null);
    setSuccess(null);
    setShowPasswordDialog(false);
    setUploadProgress(0);
  };

  const handleCloseError = () => {
    setError(null);
  };

  const handleCloseSuccess = () => {
    setSuccess(null);
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Card
        onDragEnter={handleDragEnter}
        onDragOver={(e) => e.preventDefault()}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        sx={{
          p: 4,
          border: '2px dashed #ccc',
          minHeight: 200,
          borderRadius: 2,
          textAlign: 'center',
          backgroundColor: isDragActive ? 'action.hover' : 'background.paper',
          transition: 'all 0.2s ease-in-out',
        }}
      >
        <CardContent>
          <Typography variant="h4" gutterBottom>
            DOCX to PDF Converter
          </Typography>
          <Typography variant="body1" color="text.secondary" paragraph>
            Upload a DOCX file to convert it to PDF. You can also add password protection to the PDF.
          </Typography>

          {!metadata && (
            <Box sx={{ mt: 3 }}>
              <Button
                component="label"
                variant="contained"
                startIcon={<FileUploadIcon />}
                disabled={loading}
              >
                Upload DOCX
                <VisuallyHiddenInput
                  type="file"
                  accept=".docx"
                  onChange={handleFileSelect}
                />
              </Button>
            </Box>
          )}

          {loading && (
            <Box sx={{ mt: 3 }}>
              <LinearProgress variant="determinate" value={uploadProgress} />
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                {uploadProgress}% Complete
              </Typography>
            </Box>
          )}

          {metadata && (
            <Box sx={{ mt: 3, mb: 3 }}>
              <Typography variant="body1" sx={{ mb: 1 }}>
                <strong>Filename:</strong> {metadata.filename}
              </Typography>
              <Typography variant="body1" sx={{ mb: 1 }}>
                <strong>Size:</strong> {formatBytes(metadata.size)}
              </Typography>
              <Typography variant="body1" sx={{ mb: 2 }}>
                <strong>Uploaded:</strong> {formatDate(metadata.upload_time)}
              </Typography>
              <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
                <Button
                  variant="contained"
                  startIcon={<LockIcon />}
                  onClick={() => setShowPasswordDialog(true)}
                  disabled={loading}
                >
                  Add Password
                </Button>
                <Button
                  variant="contained"
                  color="success"
                  startIcon={<DownloadIcon />}
                  onClick={handleConvert}
                  disabled={loading}
                >
                  Convert & Download
                </Button>
                <IconButton 
                  color="error" 
                  onClick={handleReset}
                  disabled={loading}
                  title="Clear"
                >
                  <DeleteIcon />
                </IconButton>
              </Box>
              {loading && <LinearProgress sx={{ mt: 2 }} />}
            </Box>
          )}
        </CardContent>
      </Card>

      <Dialog open={showPasswordDialog} onClose={() => setShowPasswordDialog(false)}>
        <DialogTitle>Password Protection (Optional)</DialogTitle>
        <DialogContent>
          <DialogContentText>
            You can add password protection to your PDF. Leave blank for no password.
          </DialogContentText>
          <TextField
            autoFocus
            margin="dense"
            label="PDF Password"
            type="password"
            fullWidth
            variant="outlined"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowPasswordDialog(false)}>Cancel</Button>
          <Button onClick={handleConvert} variant="contained" startIcon={<LockIcon />}>
            Convert to PDF
          </Button>
        </DialogActions>
      </Dialog>

      <Snackbar
        open={!!error}
        autoHideDuration={6000}
        onClose={handleCloseError}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={handleCloseError} severity="error" sx={{ width: '100%' }}>
          {error}
        </Alert>
      </Snackbar>

      <Snackbar
        open={!!success}
        autoHideDuration={6000}
        onClose={handleCloseSuccess}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={handleCloseSuccess} severity="success" sx={{ width: '100%' }}>
          {success}
        </Alert>
      </Snackbar>
    </Container>
  );
}

export default App;
