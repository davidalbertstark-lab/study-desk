import api from "./client";

export async function updateProfile(data: {
  full_name: string;
  matric_number: string;
  level: string;
  faculty: string;
  department: string;
}) {
  const res = await api.patch(
    "/users/me/profile",
    data
  );

  return res.data.data;
}