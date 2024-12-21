import React from "react";
import "tailwindcss/tailwind.css";

const ProHealthDashboard = () => {
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      {/* Header */}
      <header className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-semibold text-gray-800">ProHealth Dashboard</h1>
        <div className="flex items-center space-x-4">
          <div className="bg-white p-2 rounded-full shadow-md">
            {/* Profile Image Placeholder */}
            <img
              src="/profile-placeholder.png"
              alt="Profile"
              className="h-10 w-10 rounded-full object-cover"
            />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Section */}
        <div className="lg:col-span-2 bg-white p-6 rounded-xl shadow-md">
          <h2 className="text-lg font-medium text-gray-800 mb-4">Overview</h2>
          <div className="flex items-center justify-between">
            {/* Visualization Placeholder */}
            <div className="flex-1 h-48 bg-gray-200 rounded-lg flex items-center justify-center">
              <span className="text-gray-500">Visualization Placeholder</span>
            </div>
            <div className="ml-6">
              <h3 className="text-gray-600">Heart Rate</h3>
              <p className="text-3xl font-semibold text-gray-800">110 bpm</p>
              <h3 className="text-gray-600 mt-4">Temperature</h3>
              <p className="text-3xl font-semibold text-gray-800">34.7°C</p>
              <h3 className="text-gray-600 mt-4">Blood</h3>
              <p className="text-3xl font-semibold text-gray-800">98%</p>
            </div>
          </div>
        </div>

        {/* Right Section */}
        <div className="space-y-6">
          {/* Card 1 */}
          <div className="bg-white p-6 rounded-xl shadow-md">
            <h3 className="text-gray-600">Medication</h3>
            <div className="flex items-center justify-between mt-4">
              <p className="text-sm text-gray-500">Paracetamol</p>
              <p className="text-gray-800 font-semibold">25%</p>
            </div>
            <div className="flex items-center justify-between mt-4">
              <p className="text-sm text-gray-500">Influenza</p>
              <p className="text-gray-800 font-semibold">523 mg</p>
            </div>
          </div>

          {/* Card 2 */}
          <div className="bg-white p-6 rounded-xl shadow-md">
            <h3 className="text-gray-600">Scan</h3>
            <p className="text-gray-800 font-semibold text-2xl mt-4">Cardiology</p>
          </div>

          {/* Card 3 */}
          <div className="bg-white p-6 rounded-xl shadow-md">
            <h3 className="text-gray-600">Osteoporosis</h3>
            <div className="h-32 bg-gray-200 rounded-lg flex items-center justify-center mt-4">
              <span className="text-gray-500">Image Placeholder</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProHealthDashboard;
