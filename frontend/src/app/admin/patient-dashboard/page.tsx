'use client';

import { Box, SimpleGrid } from '@chakra-ui/react';
import AppointmentsTable from 'views/admin/patientDashboard/components/AppointmentsTable';
import PrescriptionsTable from 'views/admin/patientDashboard/components/PrescriptionsTable';
import HealthReportsTable from 'views/admin/patientDashboard/components/HealthReportsTable';
import NotificationsTable from 'views/admin/patientDashboard/components/NotificationsTable';
import appointmentsData from 'views/admin/patientDashboard/variables/appointmentsData';
import prescriptionsData from 'views/admin/patientDashboard/variables/prescriptionsData';
import healthReportsData from 'views/admin/patientDashboard/variables/healthReportsData';
import notificationsData from 'views/admin/patientDashboard/variables/notificationsData';
import React from 'react';

export default function PatientDashboard() {
  return (
    <Box pt={{ base: '130px', md: '80px', xl: '80px' }}>
      <SimpleGrid
        mb="20px"
        columns={{ sm: 1, md: 2 }}
        spacing={{ base: '20px', xl: '20px' }}
      >
        <AppointmentsTable tableData={appointmentsData} />
        <PrescriptionsTable tableData={prescriptionsData} />
        <HealthReportsTable tableData={healthReportsData} />
        <NotificationsTable tableData={notificationsData} />
      </SimpleGrid>
    </Box>
  );
}
