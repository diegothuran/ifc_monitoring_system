import React, { useState } from 'react';
import {
  Box,
  Typography,
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
  Button,
  Alert,
  CircularProgress,
} from '@mui/material';
import { CheckCircle, Cancel, Visibility } from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { api } from '../services/api';

interface Alert {
  id: number;
  title: string;
  message: string;
  sensor_id: number;
  severity: string;
  status: string;
  triggered_at: string;
  acknowledged_at?: string;
  resolved_at?: string;
  threshold_value?: number;
  actual_value?: number;
}

const Alerts: React.FC = () => {
  const [selectedAlert, setSelectedAlert] = useState<Alert | null>(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [error, setError] = useState('');

  const queryClient = useQueryClient();

  const { data: alerts, isLoading: alertsLoading, error: alertsError } = useQuery('alerts', () =>
    api.get('/alerts/').then(res => res.data)
  );

  const { data: sensors } = useQuery('sensors', () =>
    api.get('/sensors/').then(res => res.data)
  );

  const updateAlertMutation = useMutation(
    ({ id, data }: { id: number; data: any }) => api.put(`/alerts/${id}`, data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('alerts');
        setOpenDialog(false);
        setSelectedAlert(null);
      },
      onError: (error: any) => {
        setError(error.response?.data?.detail || 'Failed to update alert');
      }
    }
  );

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'error';
      case 'high': return 'error';
      case 'medium': return 'warning';
      case 'low': return 'info';
      default: return 'default';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'error';
      case 'acknowledged': return 'warning';
      case 'resolved': return 'success';
      default: return 'default';
    }
  };

  const handleAcknowledge = (alert: Alert) => {
    updateAlertMutation.mutate({
      id: alert.id,
      data: { status: 'acknowledged' }
    });
  };

  const handleResolve = (alert: Alert) => {
    updateAlertMutation.mutate({
      id: alert.id,
      data: { status: 'resolved' }
    });
  };

  const handleViewDetails = (alert: Alert) => {
    setSelectedAlert(alert);
    setOpenDialog(true);
    setError('');
  };

  const getSensorName = (sensorId: number) => {
    const sensor = sensors?.sensors?.find((s: any) => s.id === sensorId);
    return sensor ? sensor.name : `Sensor ${sensorId}`;
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Alerts
      </Typography>

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
                <TableCell>Title</TableCell>
                <TableCell>Sensor</TableCell>
                <TableCell>Severity</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Triggered</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {alertsLoading ? (
                <TableRow>
                  <TableCell colSpan={6} align="center">
                    <CircularProgress />
                  </TableCell>
                </TableRow>
              ) : alerts?.alerts?.map((alert: any) => (
                <TableRow key={alert.id}>
                  <TableCell>{alert.title}</TableCell>
                  <TableCell>{getSensorName(alert.sensor_id)}</TableCell>
                  <TableCell>
                    <Chip 
                      label={alert.severity} 
                      color={getSeverityColor(alert.severity)}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    <Chip 
                      label={alert.status} 
                      color={getStatusColor(alert.status)}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    {new Date(alert.triggered_at).toLocaleString()}
                  </TableCell>
                  <TableCell>
                    <IconButton 
                      size="small" 
                      onClick={() => handleViewDetails(alert)}
                      title="View Details"
                    >
                      <Visibility />
                    </IconButton>
                    {alert.status === 'active' && (
                      <IconButton 
                        size="small" 
                        color="primary"
                        onClick={() => handleAcknowledge(alert)}
                        title="Acknowledge"
                      >
                        <CheckCircle />
                      </IconButton>
                    )}
                    {alert.status === 'acknowledged' && (
                      <IconButton 
                        size="small" 
                        color="success"
                        onClick={() => handleResolve(alert)}
                        title="Resolve"
                      >
                        <CheckCircle />
                      </IconButton>
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>

      {/* Alert Details Dialog */}
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          Alert Details
        </DialogTitle>
        <DialogContent>
          {selectedAlert && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="h6" gutterBottom>
                {selectedAlert.title}
              </Typography>
              
              <Box sx={{ mb: 2 }}>
                <Typography variant="body1" paragraph>
                  {selectedAlert.message}
                </Typography>
              </Box>

              <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 2, mb: 2 }}>
                <Box>
                  <Typography variant="subtitle2" color="textSecondary">
                    Sensor
                  </Typography>
                  <Typography variant="body1">
                    {getSensorName(selectedAlert.sensor_id)}
                  </Typography>
                </Box>

                <Box>
                  <Typography variant="subtitle2" color="textSecondary">
                    Severity
                  </Typography>
                  <Chip 
                    label={selectedAlert.severity} 
                    color={getSeverityColor(selectedAlert.severity)}
                    size="small"
                  />
                </Box>

                <Box>
                  <Typography variant="subtitle2" color="textSecondary">
                    Status
                  </Typography>
                  <Chip 
                    label={selectedAlert.status} 
                    color={getStatusColor(selectedAlert.status)}
                    size="small"
                  />
                </Box>

                <Box>
                  <Typography variant="subtitle2" color="textSecondary">
                    Triggered At
                  </Typography>
                  <Typography variant="body1">
                    {new Date(selectedAlert.triggered_at).toLocaleString()}
                  </Typography>
                </Box>

                {selectedAlert.threshold_value && (
                  <Box>
                    <Typography variant="subtitle2" color="textSecondary">
                      Threshold Value
                    </Typography>
                    <Typography variant="body1">
                      {selectedAlert.threshold_value}
                    </Typography>
                  </Box>
                )}

                {selectedAlert.actual_value && (
                  <Box>
                    <Typography variant="subtitle2" color="textSecondary">
                      Actual Value
                    </Typography>
                    <Typography variant="body1">
                      {selectedAlert.actual_value}
                    </Typography>
                  </Box>
                )}

                {selectedAlert.acknowledged_at && (
                  <Box>
                    <Typography variant="subtitle2" color="textSecondary">
                      Acknowledged At
                    </Typography>
                    <Typography variant="body1">
                      {new Date(selectedAlert.acknowledged_at).toLocaleString()}
                    </Typography>
                  </Box>
                )}

                {selectedAlert.resolved_at && (
                  <Box>
                    <Typography variant="subtitle2" color="textSecondary">
                      Resolved At
                    </Typography>
                    <Typography variant="body1">
                      {new Date(selectedAlert.resolved_at).toLocaleString()}
                    </Typography>
                  </Box>
                )}
              </Box>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Close</Button>
          {selectedAlert?.status === 'active' && (
            <Button 
              onClick={() => handleAcknowledge(selectedAlert)} 
              variant="contained"
              color="primary"
            >
              Acknowledge
            </Button>
          )}
          {selectedAlert?.status === 'acknowledged' && (
            <Button 
              onClick={() => handleResolve(selectedAlert)} 
              variant="contained"
              color="success"
            >
              Resolve
            </Button>
          )}
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Alerts;
