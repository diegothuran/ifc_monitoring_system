import React, { useState } from 'react';
import {
  Box,
  Typography,
  Button,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  CircularProgress,
} from '@mui/material';
import { Add, Edit, Delete } from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { api } from '../services/api';

interface Sensor {
  id: number;
  name: string;
  sensor_type: string;
  device_id: string;
  location_id: number;
  is_active: boolean;
  unit?: string;
  alert_threshold_min?: number;
  alert_threshold_max?: number;
}

interface Location {
  id: number;
  name: string;
}

const Sensors: React.FC = () => {
  const [openDialog, setOpenDialog] = useState(false);
  const [editingSensor, setEditingSensor] = useState<Sensor | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    sensor_type: 'temperature',
    device_id: '',
    location_id: 1,
    unit: '',
    alert_threshold_min: '',
    alert_threshold_max: '',
  });
  const [error, setError] = useState('');

  const queryClient = useQueryClient();

  const { data: sensors, isLoading: sensorsLoading, error: sensorsError } = useQuery('sensors', () =>
    api.get('/sensors/').then(res => res.data)
  );

  const { data: locations } = useQuery('locations', () =>
    api.get('/locations/').then(res => res.data)
  );

  const createSensorMutation = useMutation(
    (data: any) => api.post('/sensors/', data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('sensors');
        setOpenDialog(false);
        setFormData({
          name: '',
          sensor_type: 'temperature',
          device_id: '',
          location_id: 1,
          unit: '',
          alert_threshold_min: '',
          alert_threshold_max: '',
        });
      },
      onError: (error: any) => {
        setError(error.response?.data?.detail || 'Failed to create sensor');
      }
    }
  );

  const updateSensorMutation = useMutation(
    ({ id, data }: { id: number; data: any }) => api.put(`/sensors/${id}`, data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('sensors');
        setOpenDialog(false);
        setEditingSensor(null);
        setFormData({
          name: '',
          sensor_type: 'temperature',
          device_id: '',
          location_id: 1,
          unit: '',
          alert_threshold_min: '',
          alert_threshold_max: '',
        });
      },
      onError: (error: any) => {
        setError(error.response?.data?.detail || 'Failed to update sensor');
      }
    }
  );

  const deleteSensorMutation = useMutation(
    (id: number) => api.delete(`/sensors/${id}`),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('sensors');
      },
      onError: (error: any) => {
        setError(error.response?.data?.detail || 'Failed to delete sensor');
      }
    }
  );

  const handleOpenDialog = (sensor?: Sensor) => {
    if (sensor) {
      setEditingSensor(sensor);
      setFormData({
        name: sensor.name,
        sensor_type: sensor.sensor_type,
        device_id: sensor.device_id,
        location_id: sensor.location_id,
        unit: sensor.unit || '',
        alert_threshold_min: sensor.alert_threshold_min?.toString() || '',
        alert_threshold_max: sensor.alert_threshold_max?.toString() || '',
      });
    } else {
      setEditingSensor(null);
      setFormData({
        name: '',
        sensor_type: 'temperature',
        device_id: '',
        location_id: 1,
        unit: '',
        alert_threshold_min: '',
        alert_threshold_max: '',
      });
    }
    setOpenDialog(true);
    setError('');
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setEditingSensor(null);
    setError('');
  };

  const handleSubmit = () => {
    const data = {
      ...formData,
      alert_threshold_min: formData.alert_threshold_min ? parseFloat(formData.alert_threshold_min) : null,
      alert_threshold_max: formData.alert_threshold_max ? parseFloat(formData.alert_threshold_max) : null,
    };

    if (editingSensor) {
      updateSensorMutation.mutate({ id: editingSensor.id, data });
    } else {
      createSensorMutation.mutate(data);
    }
  };

  const handleDelete = (id: number) => {
    if (window.confirm('Are you sure you want to delete this sensor?')) {
      deleteSensorMutation.mutate(id);
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">
          Sensors
        </Typography>
        <Button 
          variant="contained" 
          startIcon={<Add />}
          onClick={() => handleOpenDialog()}
        >
          Add Sensor
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>
          {error}
        </Alert>
      )}

      <Paper>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Name</TableCell>
                <TableCell>Type</TableCell>
                <TableCell>Device ID</TableCell>
                <TableCell>Location</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Unit</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {sensorsLoading ? (
                <TableRow>
                  <TableCell colSpan={7} align="center">
                    <CircularProgress />
                  </TableCell>
                </TableRow>
              ) : sensors?.sensors?.map((sensor: any) => (
                <TableRow key={sensor.id}>
                  <TableCell>{sensor.name}</TableCell>
                  <TableCell>
                    <Chip label={sensor.sensor_type} size="small" />
                  </TableCell>
                  <TableCell>{sensor.device_id}</TableCell>
                  <TableCell>
                    {locations?.locations?.find((loc: Location) => loc.id === sensor.location_id)?.name || `Location ${sensor.location_id}`}
                  </TableCell>
                  <TableCell>
                    <Chip 
                      label={sensor.is_active ? 'Active' : 'Inactive'} 
                      color={sensor.is_active ? 'success' : 'default'}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>{sensor.unit || '--'}</TableCell>
                  <TableCell>
                    <IconButton size="small" onClick={() => handleOpenDialog(sensor)}>
                      <Edit />
                    </IconButton>
                    <IconButton 
                      size="small" 
                      color="error"
                      onClick={() => handleDelete(sensor.id)}
                    >
                      <Delete />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>

      {/* Add/Edit Sensor Dialog */}
      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editingSensor ? 'Edit Sensor' : 'Add New Sensor'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
            <TextField
              label="Sensor Name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              fullWidth
            />
            
            <FormControl fullWidth>
              <InputLabel>Sensor Type</InputLabel>
              <Select
                value={formData.sensor_type}
                onChange={(e) => setFormData({ ...formData, sensor_type: e.target.value })}
                label="Sensor Type"
              >
                <MenuItem value="temperature">Temperature</MenuItem>
                <MenuItem value="humidity">Humidity</MenuItem>
                <MenuItem value="pressure">Pressure</MenuItem>
                <MenuItem value="light">Light</MenuItem>
                <MenuItem value="motion">Motion</MenuItem>
              </Select>
            </FormControl>

            <TextField
              label="Device ID"
              value={formData.device_id}
              onChange={(e) => setFormData({ ...formData, device_id: e.target.value })}
              fullWidth
            />

            <FormControl fullWidth>
              <InputLabel>Location</InputLabel>
              <Select
                value={formData.location_id}
                onChange={(e) => setFormData({ ...formData, location_id: e.target.value as number })}
                label="Location"
              >
                {locations?.locations?.map((location: Location) => (
                  <MenuItem key={location.id} value={location.id}>
                    {location.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <TextField
              label="Unit"
              value={formData.unit}
              onChange={(e) => setFormData({ ...formData, unit: e.target.value })}
              fullWidth
              placeholder="e.g., °C, %, hPa"
            />

            <TextField
              label="Min Alert Threshold"
              type="number"
              value={formData.alert_threshold_min}
              onChange={(e) => setFormData({ ...formData, alert_threshold_min: e.target.value })}
              fullWidth
            />

            <TextField
              label="Max Alert Threshold"
              type="number"
              value={formData.alert_threshold_max}
              onChange={(e) => setFormData({ ...formData, alert_threshold_max: e.target.value })}
              fullWidth
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button 
            onClick={handleSubmit} 
            variant="contained"
            disabled={createSensorMutation.isLoading || updateSensorMutation.isLoading}
          >
            {editingSensor ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Sensors;
