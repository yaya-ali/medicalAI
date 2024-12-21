import { Box, Table, Tbody, Td, Th, Thead, Tr, Text } from '@chakra-ui/react';

type Prescription = {
  name: string;
  dosage: string;
  frequency: string;
};

interface PrescriptionsTableProps {
  tableData: Prescription[];
}

const PrescriptionsTable: React.FC<PrescriptionsTableProps> = ({ tableData }) => {
  return (
    <Box bg="white" shadow="md" borderRadius="md" p="6">
      <Text fontSize="lg" mb="4" fontWeight="bold">
        Prescriptions
      </Text>
      <Table variant="simple">
        <Thead>
          <Tr>
            <Th>Medicine</Th>
            <Th>Dosage</Th>
            <Th>Frequency</Th>
          </Tr>
        </Thead>
        <Tbody>
          {tableData.map((row, index) => (
            <Tr key={index}>
              <Td>{row.name}</Td>
              <Td>{row.dosage}</Td>
              <Td>{row.frequency}</Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    </Box>
  );
};

export default PrescriptionsTable;
