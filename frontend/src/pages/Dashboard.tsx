import React from 'react';
import {
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  Sensors,
  Warning,
  TrendingUp,
  LocationOn,
} from '@mui/icons-material';
import { useQuery } from 'react-query';
import { api } from '../services/api';

const Dashboard: React.FC = () => {
  const { data: sensors, isLoading: sensorsLoading, error: sensorsError } = useQuery('sensors', () =>
    api.get('/sensors/?limit=10').then(res => res.data)
  );

  const { data: alerts, isLoading: alertsLoading, error: alertsError } = useQuery('alerts', () =>
    api.get('/alerts/?limit=10').then(res => res.data)
  );

  const { data: latestReadings, isLoading: readingsLoading, error: readingsError } = useQuery('latest-readings', () =>
    api.get('/readings/latest').then(res => res.data)
  );

  const { data: locations, isLoading: locationsLoading } = useQuery('locations', () =>
    api.get('/locations/?limit=10').then(res => res.data)
  );

  const stats = [
    {
      title: 'Total Sensors',
      value: sensorsLoading ? '...' : (sensors?.total || 0),
      icon: <Sensors />,
      color: '#1976d2',
      loading: sensorsLoading,
    },
    {
      title: 'Active Alerts',
      value: alertsLoading ? '...' : (alerts?.alerts?.filter((alert: any) => alert.status === 'active').length || 0),
      icon: <Warning />,
      color: '#d32f2f',
      loading: alertsLoading,
    },
    {
      title: 'Locations',
      value: locationsLoading ? '...' : (locations?.total || 0),
      icon: <LocationOn />,
      color: '#388e3c',
      loading: locationsLoading,
    },
    {
      title: 'Latest Readings',
      value: readingsLoading ? '...' : (latestReadings?.length || 0),
      icon: <TrendingUp />,
      color: '#f57c00',
      loading: readingsLoading,
    },
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      
      {/* Error handling */}
      {(sensorsError || alertsError || readingsError) && (
        <Alert severity="error" sx={{ mb: 2 }}>
          Error loading data. Please check your connection and try again.
        </Alert>
      )}
      
      <Grid container spacing={3}>
        {/* Statistics Cards */}
        {stats.map((stat, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Box sx={{ color: stat.color, mr: 2 }}>
                    {stat.icon}
                  </Box>
                  <Typography variant="h6" component="div">
                    {stat.title}
                  </Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  {stat.loading ? (
                    <CircularProgress size={24} sx={{ mr: 1 }} />
                  ) : (
                    <Typography variant="h3" component="div" color={stat.color}>
                      {stat.value}
                    </Typography>
                  )}
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}

        {/* Recent Alerts */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Recent Alerts
            </Typography>
            {alerts?.alerts?.length > 0 ? (
              <Box>
                {alerts.alerts.slice(0, 5).map((alert: any) => (
                  <Box key={alert.id} sx={{ mb: 2, p: 2, border: '1px solid #e0e0e0', borderRadius: 1 }}>
                    <Typography variant="subtitle1" color={alert.severity === 'high' ? 'error' : 'warning'}>
                      {alert.title}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      {alert.message}
                    </Typography>
                    <Typography variant="caption" color="textSecondary">
                      {new Date(alert.triggered_at).toLocaleString()}
                    </Typography>
                  </Box>
                ))}
              </Box>
            ) : (
              <Typography color="textSecondary">No recent alerts</Typography>
            )}
          </Paper>
        </Grid>

        {/* Latest Readings */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Latest Sensor Readings
            </Typography>
            {latestReadings?.length > 0 ? (
              <Box>
                {latestReadings.slice(0, 5).map((reading: any) => (
                  <Box key={reading.id} sx={{ mb: 2, p: 2, border: '1px solid #e0e0e0', borderRadius: 1 }}>
                    <Typography variant="subtitle1">
                      Sensor {reading.sensor_id}
                    </Typography>
                    <Typography variant="h6" color="primary">
                      {reading.value}
                    </Typography>
                    <Typography variant="caption" color="textSecondary">
                      {new Date(reading.timestamp).toLocaleString()}
                    </Typography>
                  </Box>
                ))}
              </Box>
            ) : (
              <Typography color="textSecondary">No recent readings</Typography>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
