interface ApiValidationResponse {
  message?: string
  errors?: Record<string, string>
}

const formService = {
  handleError(
    error: any,
    errors: Record<string, string>,
    defaultMessage = 'Ocorreu um erro. Tente novamente.'
  ): string {
    if (error.response?.data) {
      const data: ApiValidationResponse = error.response.data

      if (data.errors) {
  console.log(errors)

        Object.assign(errors, data.errors)
      }

      return data.message || defaultMessage
    }

    return 'Erro de conexão. Verifique sua internet.'
  },

  clearErrors(errors: Record<string, string>) {
    Object.keys(errors).forEach((key) => {
      delete errors[key]
    })
  }
}

export default formService
