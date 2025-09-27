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
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Alert,
  CircularProgress,
} from '@mui/material';
import { Add, Edit, Delete } from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { api } from '../services/api';

interface Location {
  id: number;
  name: string;
  description?: string;
  building?: string;
  floor?: string;
  room?: string;
  zone?: string;
  responsible_person?: string;
  phone?: string;
  email?: string;
}

const Locations: React.FC = () => {
  const [openDialog, setOpenDialog] = useState(false);
  const [editingLocation, setEditingLocation] = useState<Location | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    building: '',
    floor: '',
    room: '',
    zone: '',
    responsible_person: '',
    phone: '',
    email: '',
  });
  const [error, setError] = useState('');

  const queryClient = useQueryClient();

  const { data: locations, isLoading: locationsLoading, error: locationsError } = useQuery('locations', () =>
    api.get('/locations/').then(res => res.data)
  );

  const createLocationMutation = useMutation(
    (data: any) => api.post('/locations/', data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('locations');
        setOpenDialog(false);
        setFormData({
          name: '',
          description: '',
          building: '',
          floor: '',
          room: '',
          zone: '',
          responsible_person: '',
          phone: '',
          email: '',
        });
      },
      onError: (error: any) => {
        setError(error.response?.data?.detail || 'Failed to create location');
      }
    }
  );

  const updateLocationMutation = useMutation(
    ({ id, data }: { id: number; data: any }) => api.put(`/locations/${id}`, data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('locations');
        setOpenDialog(false);
        setEditingLocation(null);
        setFormData({
          name: '',
          description: '',
          building: '',
          floor: '',
          room: '',
          zone: '',
          responsible_person: '',
          phone: '',
          email: '',
        });
      },
      onError: (error: any) => {
        setError(error.response?.data?.detail || 'Failed to update location');
      }
    }
  );

  const deleteLocationMutation = useMutation(
    (id: number) => api.delete(`/locations/${id}`),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('locations');
      },
      onError: (error: any) => {
        setError(error.response?.data?.detail || 'Failed to delete location');
      }
    }
  );

  const handleOpenDialog = (location?: Location) => {
    if (location) {
      setEditingLocation(location);
      setFormData({
        name: location.name,
        description: location.description || '',
        building: location.building || '',
        floor: location.floor || '',
        room: location.room || '',
        zone: location.zone || '',
        responsible_person: location.responsible_person || '',
        phone: location.phone || '',
        email: location.email || '',
      });
    } else {
      setEditingLocation(null);
      setFormData({
        name: '',
        description: '',
        building: '',
        floor: '',
        room: '',
        zone: '',
        responsible_person: '',
        phone: '',
        email: '',
      });
    }
    setOpenDialog(true);
    setError('');
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setEditingLocation(null);
    setError('');
  };

  const handleSubmit = () => {
    const data = {
      ...formData,
      // Remove empty strings and convert to null
      description: formData.description || null,
      building: formData.building || null,
      floor: formData.floor || null,
      room: formData.room || null,
      zone: formData.zone || null,
      responsible_person: formData.responsible_person || null,
      phone: formData.phone || null,
      email: formData.email || null,
    };

    if (editingLocation) {
      updateLocationMutation.mutate({ id: editingLocation.id, data });
    } else {
      createLocationMutation.mutate(data);
    }
  };

  const handleDelete = (id: number) => {
    if (window.confirm('Are you sure you want to delete this location?')) {
      deleteLocationMutation.mutate(id);
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">
          Locations
        </Typography>
        <Button 
          variant="contained" 
          startIcon={<Add />}
          onClick={() => handleOpenDialog()}
        >
          Add Location
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
                <TableCell>Building</TableCell>
                <TableCell>Floor</TableCell>
                <TableCell>Room</TableCell>
                <TableCell>Zone</TableCell>
                <TableCell>Responsible Person</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {locationsLoading ? (
                <TableRow>
                  <TableCell colSpan={7} align="center">
                    <CircularProgress />
                  </TableCell>
                </TableRow>
              ) : locations?.locations?.map((location: any) => (
                <TableRow key={location.id}>
                  <TableCell>{location.name}</TableCell>
                  <TableCell>{location.building || '--'}</TableCell>
                  <TableCell>{location.floor || '--'}</TableCell>
                  <TableCell>{location.room || '--'}</TableCell>
                  <TableCell>{location.zone || '--'}</TableCell>
                  <TableCell>{location.responsible_person || '--'}</TableCell>
                  <TableCell>
                    <IconButton size="small" onClick={() => handleOpenDialog(location)}>
                      <Edit />
                    </IconButton>
                    <IconButton 
                      size="small" 
                      color="error"
                      onClick={() => handleDelete(location.id)}
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

      {/* Add/Edit Location Dialog */}
      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editingLocation ? 'Edit Location' : 'Add New Location'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
            <TextField
              label="Location Name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              fullWidth
              required
            />
            
            <TextField
              label="Description"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              fullWidth
              multiline
              rows={2}
            />

            <TextField
              label="Building"
              value={formData.building}
              onChange={(e) => setFormData({ ...formData, building: e.target.value })}
              fullWidth
            />

            <TextField
              label="Floor"
              value={formData.floor}
              onChange={(e) => setFormData({ ...formData, floor: e.target.value })}
              fullWidth
            />

            <TextField
              label="Room"
              value={formData.room}
              onChange={(e) => setFormData({ ...formData, room: e.target.value })}
              fullWidth
            />

            <TextField
              label="Zone"
              value={formData.zone}
              onChange={(e) => setFormData({ ...formData, zone: e.target.value })}
              fullWidth
            />

            <TextField
              label="Responsible Person"
              value={formData.responsible_person}
              onChange={(e) => setFormData({ ...formData, responsible_person: e.target.value })}
              fullWidth
            />

            <TextField
              label="Phone"
              value={formData.phone}
              onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
              fullWidth
            />

            <TextField
              label="Email"
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              fullWidth
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button 
            onClick={handleSubmit} 
            variant="contained"
            disabled={createLocationMutation.isLoading || updateLocationMutation.isLoading}
          >
            {editingLocation ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Locations;
