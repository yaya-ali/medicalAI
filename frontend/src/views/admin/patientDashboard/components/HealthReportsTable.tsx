import { Box, Table, Tbody, Td, Th, Thead, Tr, Text } from '@chakra-ui/react';

type HealthReport = {
  report: string;
  date: string;
};

interface HealthReportsTableProps {
  tableData: HealthReport[];
}

const HealthReportsTable: React.FC<HealthReportsTableProps> = ({ tableData }) => {
  return (
    <Box bg="white" shadow="md" borderRadius="md" p="6">
      <Text fontSize="lg" mb="4" fontWeight="bold">
        Health Reports
      </Text>
      <Table variant="simple">
        <Thead>
          <Tr>
            <Th>Report</Th>
            <Th>Date</Th>
          </Tr>
        </Thead>
        <Tbody>
          {tableData.map((row, index) => (
            <Tr key={index}>
              <Td>{row.report}</Td>
              <Td>{row.date}</Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    </Box>
  );
};

export default HealthReportsTable;
