import { Box, Text, Heading } from '@chakra-ui/react';

interface DashboardCardProps {
  title: string;
  value: string | number;
}

export default function DashboardCard({ title, value }: DashboardCardProps) {
  return (
    <Box
      bg="white"
      shadow="md"
      borderRadius="md"
      p="6"
      textAlign="center"
    >
      <Heading fontSize="lg" mb="2">
        {title}
      </Heading>
      <Text fontSize="2xl" fontWeight="bold" color="blue.500">
        {value}
      </Text>
    </Box>
  );
}
