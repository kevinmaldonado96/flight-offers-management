package com.uniandes.cloud.rf04.models

import com.uniandes.cloud.rf04.enums.UserStatus

data class CurrentUser(
    val id: String,
    val username: String,
    val email: String,
    val dni: String?,
    val fullName: String?,
    val phoneNumber: String?,
    val status: UserStatus?
)

