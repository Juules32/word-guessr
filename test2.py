#!/usr/bin/env python3
# Python imports
from typing import Optional
# Packages imports
from pydantic import BaseModel, field_validator

class B(BaseModel):
    var3: str
    var4: str

class A(BaseModel):
    var1: int
    var2: Optional[B] = None

    @field_validator('var2', mode='before')
    def check_empty(cls, value):
        print("check_empty", cls, value)
        return value or None

if __name__ == "__main__":
    data = {
        "var1": 1,
        "var2": {}
    }
    result = A.model_validate(data)
    print(result)