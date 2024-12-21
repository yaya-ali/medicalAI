import { Box, List, ListItem, Text } from '@chakra-ui/react';

type Notification = {
  message: string;
};

interface NotificationsTableProps {
  tableData: Notification[];
}

const NotificationsTable: React.FC<NotificationsTableProps> = ({ tableData }) => {
  return (
    <Box bg="white" shadow="md" borderRadius="md" p="6">
      <Text fontSize="lg" mb="4" fontWeight="bold">
        Notifications
      </Text>
      <List spacing={3}>
        {tableData.map((row, index) => (
          <ListItem key={index}>{row.message}</ListItem>
        ))}
      </List>
    </Box>
  );
};

export default NotificationsTable;
