export const healthService = {
  check() {
    return { status: 'ok', time: new Date().toISOString() };
  },
};
