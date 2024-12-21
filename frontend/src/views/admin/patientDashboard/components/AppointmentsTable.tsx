import { Box, Table, Tbody, Td, Th, Thead, Tr, Text } from '@chakra-ui/react';

type Appointment = {
  date: string;
  time: string;
  doctor: string;
};

interface AppointmentsTableProps {
  tableData: Appointment[];
}

const AppointmentsTable: React.FC<AppointmentsTableProps> = ({ tableData }) => {
  return (
    <Box bg="white" shadow="md" borderRadius="md" p="6">
      <Text fontSize="lg" mb="4" fontWeight="bold">
        Upcoming Appointments
      </Text>
      <Table variant="simple">
        <Thead>
          <Tr>
            <Th>Date</Th>
            <Th>Time</Th>
            <Th>Doctor</Th>
          </Tr>
        </Thead>
        <Tbody>
          {tableData.map((row, index) => (
            <Tr key={index}>
              <Td>{row.date}</Td>
              <Td>{row.time}</Td>
              <Td>{row.doctor}</Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    </Box>
  );
};

export default AppointmentsTable;
